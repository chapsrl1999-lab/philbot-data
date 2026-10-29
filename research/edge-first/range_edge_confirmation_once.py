#!/usr/bin/env python3
"""One frozen 4h reversal-confirmation test, after the first edge-first lab."""
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from range_edge_once import (SYMBOLS, YEAR_MONTHS, H, INTERVAL_MS, SEED,
                             download, build_events, average, roundn, percentile)

OUT=Path('research/edge-first/confirmation_results_20261029.json')

def outcome(bars,r):
    i=r['i']
    if i+7 >= len(bars) or bars[i+7][0]-bars[i][0] != 7*INTERVAL_MS:
        return None
    move=bars[i+1][4]-bars[i][4]
    direction=1 if r['side']=='LONG' else -1
    confirmed=direction*move>0
    entry=bars[i+2][1]
    final=bars[i+7][4]
    if entry<=0 or final<=0:
        return None
    profit=direction*(final/entry-1)*100-.20
    return {'confirmed':confirmed,'net':profit,'gross':profit+.20}

def stats(arr, seed):
    if not arr:return {'n':0}
    r=[x['net'] for x in arr]
    valid=[x for x in arr if x.get('control_mean') is not None]
    diff=[x['net']-x['control_mean'] for x in valid]
    clusters=defaultdict(list)
    for x in valid: clusters[x['week']].append(x['net']-x['control_mean'])
    weeks=list(clusters.values());rng=random.Random(seed);sims=[]
    for _ in range(2000):
        sample=[]
        for _ in weeks:sample.extend(weeks[rng.randrange(len(weeks))])
        if sample:sims.append(sum(sample)/len(sample))
    return {'n':len(arr),'n_matched':len(valid),
            'mean_net_pct':roundn(average(r)),'median_net_pct':roundn(statistics.median(r)),
            'win_pct':roundn(sum(x>0 for x in r)*100/len(r),2),
            'matched_control_net_pct':roundn(average([x['control_mean'] for x in valid])),
            'excess_vs_control_pct_points':roundn(average(diff)),
            'bootstrap_95pct_excess': [roundn(percentile(sims,.025)),roundn(percentile(sims,.975))],
            'n_calendar_weeks':len(weeks),'mean_net_cost0p4_pct':roundn(average(r)-.20),
            'mean_net_cost0p8_pct':roundn(average(r)-.60)}

def main():
    todo=[(s,y,m) for s in SYMBOLS for y,m in YEAR_MONTHS]
    dat=defaultdict(list);bad=[];digests={}
    with ThreadPoolExecutor(max_workers=6) as p:
        fs=[p.submit(download,q) for q in todo]
        for f in as_completed(fs):
            key,bars,err,digest=f.result()
            if err:bad.append({'key':key,'reason':err})
            else:
                dat[key[0]].extend(bars)
                digests[f'{key[0]}-{key[1]}-{key[2]:02d}']=digest
    summary=[];all_events=[]
    for asset in SYMBOLS:
        series=sorted(dat[asset]);raw_events,baseline=build_events(series,asset)
        pool=defaultdict(list)
        for base in baseline:
            out=outcome(series,base)
            if out is not None and out['confirmed']:
                pool[(base['month'],base['side'])].append((base,out['net']))
        confirmed=unconfirmed=0;unmatched=0
        for e in raw_events:
            out=outcome(series,e)
            if out is None:continue
            e=dict(e);e.update(out)
            if out['confirmed']:
                candidates=[pnl for b,pnl in pool[(e['month'],e['side'])]
                        if .6*e['vol']<=b['vol']<=1.4*e['vol'] and abs(e['i']-b['i'])>=H]
                e['control_mean']=average(candidates)
                if not candidates:unmatched+=1
                confirmed+=1
            else:
                e['control_mean']=None
                unconfirmed+=1
            all_events.append(e)
        summary.append({'asset':asset,'raw_original_events':len(raw_events),
                        'confirmed_events':confirmed,'unconfirmed_events':unconfirmed,
                        'confirmed_unmatched_control':unmatched,
                        'bars':len(series)})
    is_year=lambda e,y:e['year']==y and (y!=2026 or '2026-07'<=e['month']<='2026-09')
    years={}
    for y in (2024,2025,2026):
        valid=[x for x in all_events if is_year(x,y)]
        con=[x for x in valid if x['confirmed']]
        un=[x for x in valid if not x['confirmed']]
        years[str(y)]={'events_total':len(valid),
                       'confirmed':stats(con,SEED+y),
                       'unconfirmed_same_delayed_entry':stats(un,SEED+y+100),
                       'by_side':{side:stats([x for x in con if x['side']==side],SEED+y+199) for side in ('LONG','SHORT')},
                       'by_symbol':{sym:stats([x for x in con if x['asset']==sym],SEED+y+7) for sym in SYMBOLS}}
    report={'schema':'philbot.edge-first.confirmation-only.v1',
            'generated_utc':datetime.now(timezone.utc).isoformat(),
            'pre_registered':'research/edge-first/confirmation_pre_register.md',
            'original_protocol':'research/edge-first/range_edge_once.py',
            'source':'Binance official USD-M futures 4h monthly zip; each SHA256 CHECKSUM verified',
            'downloads_requested':len(todo),'downloads_verified':len(todo)-len(bad),
            'failures':bad,'sha256_manifest':digests,
            'rules':'Original extreme in 4h range; confirm if next complete 4h close moves in direction of mean; enter at subsequent open i+2 for ALL groups; exit at close i+7; cost 0.2 percentage point',
            'controls':'nonextreme with same asset/month/side/range and identical confirmation; volatility +/-40%, not within 24h of original extreme',
            'universe':summary,'years':years,
            'limitations':['Observational 24h return, no actual stops/fills/funding/liquidation; not a bot.',
                           '2026 prior work contamination and sample size; no pristine future test.',
                           'Still a fixed surviving 2026 universe and historical archive; delistings and realistic capacity need audit.',
                           'Week-cluster bootstrap handles synchronized multiasset calendar weeks imperfectly; model uncertainty remains.',
                           'No threshold tuning was allowed after seeing first experiment results.']}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PHILBOT_CONFIRMATION_ONLY='+json.dumps({y:{'n':d['events_total'],
                 'confirmed':d['confirmed'],'unconfirmed':d['unconfirmed_same_delayed_entry']} for y,d in years.items()},ensure_ascii=False))
    if bad:raise SystemExit(f'RESOURCE_CHECK_FAILURE: {len(bad)} archives; see saved results')

if __name__=='__main__':main()