#!/usr/bin/env python3
"""PhilBot independent edge-first event study. Research only: no trading APIs."""
import csv
import hashlib
import io
import json
import math
import random
import re
import statistics
import time
import urllib.error
import urllib.request
import zipfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

SYMBOLS = ('BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT',
           'DOGEUSDT', 'AVAXUSDT', 'LINKUSDT', 'LTCUSDT', 'DOTUSDT', 'BCHUSDT')
YEAR_MONTHS = [(2023, 12)] + [(y, m) for y in (2024, 2025, 2026) for m in range(1, 13 if y < 2026 else 10)]
INTERVAL_MS = 4 * 3600 * 1000
H = 6                   # 24 hours
N = 12                  # 48-hour EMA and efficiency
THRESHOLD = 1.5         # ATR deviation, frozen before downloads
RANGE_ER_MAX = 0.25
ROUND_TRIP_COST_PCT = 0.20
SEED = 20261029
SOURCE = 'https://data.binance.vision/data/futures/um/monthly/klines'
OUTPUT = Path('research/edge-first/results_20261029.json')

def fetch_bytes(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'PhilBotResearch-EdgeFirst/1.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=22) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            if attempt == 2:
                raise
        except (TimeoutError, OSError):
            if attempt == 2:
                raise
        time.sleep(0.7 * (attempt + 1))

def download(pair):
    symbol, year, month = pair
    ym = f'{year}-{month:02d}'
    name = f'{symbol}-4h-{ym}.zip'
    u = f'{SOURCE}/{symbol}/4h/{name}'
    try:
        raw = fetch_bytes(u)
        if raw is None:
            return pair, None, f'MISSING_HTTP404:{name}', None
        check = fetch_bytes(u + '.CHECKSUM')
        if check is None:
            return pair, None, f'MISSING_CHECKSUM:{name}', None
        expected = check.decode('utf-8', 'replace').strip().split()[0].lower()
        digest = hashlib.sha256(raw).hexdigest()
        if not re.fullmatch('[a-f0-9]{64}', expected) or digest != expected:
            return pair, None, f'CHECKSUM_MISMATCH:{name}', None
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            files = [x for x in z.namelist() if x.endswith('.csv')]
            if len(files) != 1:
                return pair, None, f'CSV_COUNT:{name}', None
            with z.open(files[0]) as content:
                lines = list(csv.reader(io.TextIOWrapper(content, encoding='utf-8-sig')))
        arr = []
        for line in lines:
            if len(line) < 5:
                continue
            try:
                t = int(line[0])
                if t > 10**14:
                    t //= 1000
                o, hi, lo, cl = map(float, line[1:5])
                if not (o > 0 and hi >= max(o,cl) and lo <= min(o,cl) and lo > 0):
                    raise ValueError('OHLC invalid')
                arr.append((t, o, hi, lo, cl))
            except ValueError:
                if line[0].lower().replace(' ', '') in ('open_time', 'opentime', 'timestamp'):
                    continue
                return pair, None, f'CSV_INVALID:{name}', None
        if not arr:
            return pair, None, f'EMPTY:{name}', None
        return pair, arr, None, digest
    except Exception as exc:
        return pair, None, f'READ_ERROR:{name}:{type(exc).__name__}:{str(exc)[:80]}', None

def build_events(data, symbol):
    ema = data[0][4]
    atrs = []
    base = []
    events = []
    streak = 0
    last_event = -(10**8)
    for i in range(1, len(data)-H):
        t, o, hi, lo, c = data[i]
        pt, po, phi, plo, pc = data[i-1]
        streak = (streak + 1) if t - pt == INTERVAL_MS else 0
        tr = max(hi - lo, abs(hi - pc), abs(lo - pc))
        atrs.append(tr)
        if len(atrs) > 14:
            atrs.pop(0)
        atr = sum(atrs)/len(atrs)
        # The bar i is complete; only information at/before its close is used.
        # H-horizon outcome always requires continuous bar opens and the next open.
        if streak >= 180 and data[i+H][0] - t == H*INTERVAL_MS and atr > 0:
            travel = sum(abs(data[k][4]-data[k-1][4]) for k in range(i-N+1, i+1))
            er = abs(c-data[i-N][4])/max(travel, 1e-12)
            z = (c-ema)/atr
            if er <= RANGE_ER_MAX:
                side = 'SHORT' if z > 0 else 'LONG'
                direction = -1 if side == 'SHORT' else 1
                entry = data[i+1][1]   # Next bar open; not signal close
                exit_price = data[i+H][4]  # 24h forward close
                gross = direction*(exit_price/entry - 1)*100
                day = datetime.fromtimestamp(t/1000, tz=timezone.utc)
                row = dict(asset=symbol, ts=t, i=i, month=day.strftime('%Y-%m'),
                           year=day.year, week=day.strftime('%G-W%V'),
                           side=side, z=z, efficiency=er, vol=atr/c,
                           gross=gross, net=gross-ROUND_TRIP_COST_PCT)
                if 0.25 <= abs(z) < THRESHOLD:
                    base.append(row)
                elif abs(z) >= THRESHOLD and i-last_event >= H:
                    events.append(row)
                    last_event = i
        ema += 2/(N+1)*(c-ema)
    return events, base

def average(xs):
    return sum(xs)/len(xs) if xs else None

def percentile(xs, frac):
    if not xs:
        return None
    vals = sorted(xs)
    return vals[int((len(vals)-1)*frac)]

def roundn(value, digits=4):
    return round(value,digits) if value is not None else None

def summarize(rows, year):
    group = [r for r in rows if r['year']==year]
    if not group:
        return {'n':0}
    arr = [r['net'] for r in group]
    matches = [r for r in group if r.get('control_mean') is not None]
    differences = [r['net']-r['control_mean'] for r in matches]
    # Bootstrap by calendar week. Events across coins in same week share one block.
    blocks = defaultdict(list)
    for r in matches:
        blocks[r['week']].append(r['net']-r['control_mean'])
    weeks = list(blocks.values())
    rng = random.Random(SEED + year + len(group))
    boot=[]
    for _ in range(2000):
        sampled=[]
        for _ in weeks:
            sampled.extend(weeks[rng.randrange(len(weeks))])
        if sampled:
            boot.append(sum(sampled)/len(sampled))
    return {'n':len(group), 'n_matched':len(matches),
            'mean_net_pct':roundn(average(arr)),
            'median_net_pct':roundn(statistics.median(arr)),
            'pct_net_positive':roundn(100*sum(x>0 for x in arr)/len(arr),2),
            'matched_mean_net_pct':roundn(average([r['net'] for r in matches])),
            'matched_control_net_pct':roundn(average([r['control_mean'] for r in matches])),
            'matched_excess_pct_points':roundn(average(differences)),
            'excess_95pct_week_bootstrap': [roundn(percentile(boot,.025)),roundn(percentile(boot,.975))],
            'n_weeks_with_matched_events':len(weeks),
            'net_if_cost_0p40_pct':roundn(average(arr)-.20),
            'net_if_cost_0p80_pct':roundn(average(arr)-.60)}

def analyze(all_data, statuses):
    rows=[]
    universe=[]
    for symbol, data in sorted(all_data.items()):
        uniq={r[0]:r for r in data}
        series=sorted(uniq.values())
        gaps=[(series[k-1][0],series[k][0]) for k in range(1,len(series))
              if series[k][0]-series[k-1][0]!=INTERVAL_MS]
        if len(uniq)!=len(data):
            universe.append({'symbol':symbol,'status':'REJECT_DUPLICATES','raw':len(data)})
            continue
        events, baseline=build_events(series, symbol)
        bymonth=defaultdict(list)
        for x in baseline:
            bymonth[(x['month'],x['side'])].append(x)
        for event in events:
            candidates=[b for b in bymonth.get((event['month'],event['side']),[])
                        if .60*event['vol']<=b['vol']<=1.40*event['vol']
                        and abs(b['i']-event['i'])>=H]
            event['control_mean']=average([b['net'] for b in candidates])
            event['n_controls']=len(candidates)
            rows.append(event)
        universe.append({'symbol':symbol,'n_4h_bars':len(series),'start_utc':datetime.fromtimestamp(series[0][0]/1000,timezone.utc).isoformat(),
             'end_utc':datetime.fromtimestamp(series[-1][0]/1000,timezone.utc).isoformat(),
             'gaps':len(gaps),'n_range_events':len(events),'n_range_baselines':len(baseline),
             'n_events_unmatched':sum(e['control_mean'] is None for e in events)})
    windows={2024:'2024-01-01 to 2024-12-31',2025:'2025-01-01 to 2025-12-31',2026:'2026-07-01 to 2026-09-30'}
    selected=[x for x in rows if x['year'] in (2024,2025) or (x['year']==2026 and '2026-07'<=x['month']<='2026-09')]
    return {
      'study':'PhilBot EDGE_FIRST independent observational event/control test',
      'created_utc':datetime.now(timezone.utc).isoformat(),
      'not_trading_bot':True,'trade_system_changed':False,
      'parameter_freeze':{'interval':'4h','equilibrium':'EMA12 prior close',
         'excursion_abs_z_min':THRESHOLD,'atr':'SMA14 TR including signal bar',
         'range_efficiency_48h_max':RANGE_ER_MAX,'event_spacing_hours':24,
         'outcome':'next 4h bar open to 24h after signal at close, directional return',
         'cost_roundtrip_pct_points':ROUND_TRIP_COST_PCT,
         'comparison':'same symbol, month, direction, low-efficiency regime, ATR/close within +/-40%, nonextreme abs(z) 0.25..1.5; exclude 24h from event',
         'ci':'2000 week-block bootstrap replicates, cluster synchronized symbols by calendar week'},
      'source':'official Binance data.binance.vision USD-M perpetual 4h monthly zip with sha256 CHECKSUM',
      'months_requested':len(YEAR_MONTHS),'universe_requested':list(SYMBOLS),
      'downloads':statuses,'universe':universe,
      'years':{str(y):dict(window=windows[y],all=summarize(selected,y),
         long=summarize([x for x in selected if x['side']=='LONG'],y),
         short=summarize([x for x in selected if x['side']=='SHORT'],y),
         by_symbol={s:summarize([x for x in selected if x['asset']==s],y)
                    for s in SYMBOLS}) for y in (2024,2025,2026)},
      'limitations':[
        'Exploratory. The fixed basket consists of coins still well known in 2026; survivorship bias is not eliminated.',
        'A close-based forward return is not a position execution: no stops, fills, leverage, funding, liquidation, margin, or latency.',
        '0.20 percentage point roundtrip cost is a proxy, not account-specific actual taker/maker rates.',
        'Historical exchange OHLCV intrabar execution path is not known. UTC and Binance futures cannot be equated with Bitunix or Hyperliquid.',
        'Controls are observational and may differ in unobserved characteristics. Time overlap between different coins remains; CI clusters calendar weeks.',
        'Year 2026 was already explored in prior research; this is not a pristine out-of-sample validation.',
        'Confidence intervals shown are conditional on fixed event definition; many prior strategy tests mean no discovery-level significance claim.'
      ]}

def main():
    start=time.time()
    out=defaultdict(list)
    months=[]
    todo=[(s,y,m) for s in SYMBOLS for y,m in YEAR_MONTHS]
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures=[pool.submit(download,p) for p in todo]
        for f in as_completed(futures):
            pair, bars, error, digest=f.result()
            if bars:
                out[pair[0]].extend(bars)
                months.append({'asset':pair[0],'ym':f'{pair[1]}-{pair[2]:02d}',
                               'rows':len(bars),'sha256':digest,'status':'VERIFIED'})
            else:
                months.append({'asset':pair[0],'ym':f'{pair[1]}-{pair[2]:02d}',
                               'status':'UNAVAILABLE','reason':error})
    months.sort(key=lambda x:(x['asset'],x['ym']))
    report=analyze(out,{'requested':len(todo),'verified':sum(x['status']=='VERIFIED' for x in months),
                        'failures':[x for x in months if x['status']!='VERIFIED'],
                        'manifest':months,'seconds':round(time.time()-start,2)})
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    compact={y:report['years'][y]['all'] for y in report['years']}
    print('PHILBOT_EDGE_FIRST_RESULTS='+json.dumps({'verification':report['downloads']['verified'],
        'requested':len(todo),'years':compact},ensure_ascii=False))
    if report['downloads']['verified'] < len(todo)*.9:
        raise SystemExit('INSUFFICIENT_SOURCE_COVERAGE: research report saved with explicit gaps')

if __name__=='__main__':
    main()