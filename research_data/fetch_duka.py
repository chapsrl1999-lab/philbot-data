"""Télécharge l'historique horaire Dukascopy (fichiers mensuels BID_candles_hour_1.bi5) 2015 → aujourd'hui,
plus les bougies 1 min des 3 dernières années pour les marchés principaux (pour bâtir du 5/15 min).
Format bi5 = LZMA ; enregistrements 24 octets : temps (s, int32), open, close, low, high (int32 en points), volume (float32)."""
import os, lzma, struct, time, gzip, csv, datetime as dt, urllib.request
OUT = "data/duka"; os.makedirs(OUT, exist_ok=True)
BASE = "https://datafeed.dukascopy.com/datafeed"
INSTR = ["BRENTCMDUSD", "LIGHTCMDUSD", "GASCMDUSD", "DIESELCMDUSD", "XAUUSD", "XAGUSD", "COPPERCMDUSD", "XPTCMDUSD", "XPDCMDUSD",
         "SOYBEANCMDUSX", "WHEATCMDUSX", "CORNCMDUSX", "SUGARCMDUSD", "COCOACMDUSD", "COFFEECMDUSX", "COTTONCMDUSX", "OJUICECMDUSX",
         "USA500IDXUSD", "USATECHIDXUSD", "USA30IDXUSD", "USSC2000IDXUSD", "DEUIDXEUR", "GBRIDXGBP", "FRAIDXEUR", "JPNIDXJPY", "HKGIDXHKD",
         "EUSIDXEUR", "AUSIDXAUD", "CHEIDXCHF", "ESPIDXEUR", "VOLIDXUSD", "DOLLARIDXUSD",
         "EURUSD", "USDJPY", "GBPUSD", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "EURJPY", "EURGBP", "GBPJPY", "BTCUSD", "ETHUSD"]
MINUTE = ["BRENTCMDUSD", "LIGHTCMDUSD", "GASCMDUSD", "XAUUSD", "XAGUSD", "USA500IDXUSD", "USATECHIDXUSD", "USA30IDXUSD", "DEUIDXEUR", "EURUSD", "USDJPY", "GBPUSD"]

def get(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404: return b""
            time.sleep(2 * (k + 1))
        except Exception: time.sleep(2 * (k + 1))
    return None

def parse(raw, t0):
    if not raw: return []
    data = lzma.decompress(raw); out = []
    for i in range(0, len(data) - 23, 24):
        s, o, c, l, h, v = struct.unpack(">iiiiif", data[i:i + 24])
        out.append([t0 + s, o, h, l, c, round(v, 4)])
    return out

def month_from_minutes(ins, y, m):
    """Repli quand le fichier horaire du mois manque : agrège les fichiers 1 min journaliers en bougies horaires."""
    out = []; d = dt.datetime(y, m + 1, 1)
    while d.month == m + 1:
        raw = get(f"{BASE}/{ins}/{d.year}/{m:02d}/{d.day:02d}/BID_candles_min_1.bi5"); time.sleep(0.05)
        if raw:
            t0 = int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp()); bars = {}
            for t, o, h, l, c, v in parse(raw, t0):
                k = t - t % 3600; b = bars.get(k)
                if b is None: bars[k] = [k, o, h, l, c, v]
                else: b[2] = max(b[2], h); b[3] = min(b[3], l); b[4] = c; b[5] = round(b[5] + v, 4)
            out += [bars[k] for k in sorted(bars)]
        d += dt.timedelta(days=1)
    return out

import sys
log = []; now = dt.datetime.utcnow()
ONLY = os.environ.get("INSTR")
if ONLY: INSTR = [ONLY]; MINUTE = [m for m in MINUTE if m == ONLY] if os.environ.get("WITH_MINUTE") == "1" else []
from concurrent.futures import ThreadPoolExecutor
DEADLINE = time.time() + 35 * 60; T0 = time.time()
os.makedirs('data', exist_ok=True)
def one_month(args):
    ins, y, m = args
    raw = get(f"{BASE}/{ins}/{y}/{m:02d}/BID_candles_hour_1.bi5")
    t0 = int(dt.datetime(y, m + 1, 1, tzinfo=dt.timezone.utc).timestamp())
    got = parse(raw, t0) if raw else []
    # repli minute seulement si le mois horaire est vide (les actions n'ont que ~150 bougies/mois, c'est normal)
    if not got and raw is None and time.time() < DEADLINE:   # repli minute seulement sur erreur réseau, pas sur 404
        got = month_from_minutes(ins, y, m)
    return (y, m, got, raw is None)
for ins in INSTR:
    jobs = [(ins, y, m) for y in range(2015, now.year + 1) for m in range(12) if dt.datetime(y, m + 1, 1) <= now]
    with ThreadPoolExecutor(8) as ex: res = sorted(ex.map(one_month, jobs))
    rows = [r for _, _, g, _ in res for r in g]; miss = sum(1 for *_, e in res if e)
    if rows:
        with gzip.open(f"{OUT}/{ins}_1h.csv.gz", "wt", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "o", "h", "l", "c", "v"]); w.writerows(rows)
    log.append(f"{ins} 1h: {len(rows)} bougies, {miss} échecs réseau, {sum(1 for _,_,g,_ in res if g)} mois avec données, {time.time()-T0:.0f} s")
    open('data/DUKA_LOG.txt', 'w').write('\n'.join(log))
    print(log[-1], flush=True)

start = now - dt.timedelta(days=3 * 365)
for ins in MINUTE:
    rows = []; d = start; miss = 0
    while d <= now:
        if d.weekday() < 6 or True:
            raw = get(f"{BASE}/{ins}/{d.year}/{d.month - 1:02d}/{d.day:02d}/BID_candles_min_1.bi5")
            if raw is None: miss += 1
            else:
                t0 = int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp()); rows += parse(raw, t0)
        d += dt.timedelta(days=1)
    if rows:
        with gzip.open(f"{OUT}/{ins}_1m.csv.gz", "wt", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "o", "h", "l", "c", "v"]); w.writerows(rows)
    log.append(f"{ins} 1m: {len(rows)} bougies, {miss} échecs"); print(log[-1], flush=True)
open("data/DUKA_LOG.txt", "w").write("\n".join(log))
