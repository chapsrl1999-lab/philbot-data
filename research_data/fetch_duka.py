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

def get(url, tries=8):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404: return b""
            time.sleep(3 * (k + 1))
        except Exception: time.sleep(3 * (k + 1))
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
for ins in INSTR:
    rows = []; miss = 0
    for y in range(2015, now.year + 1):
        for m in range(12):
            if dt.datetime(y, m + 1, 1) > now: break
            raw = get(f"{BASE}/{ins}/{y}/{m:02d}/BID_candles_hour_1.bi5")
            time.sleep(0.05)
            t0 = int(dt.datetime(y, m + 1, 1, tzinfo=dt.timezone.utc).timestamp())
            got = parse(raw, t0) if raw else []
            if len(got) < 300 and dt.datetime(y, m + 1, 1) < now - dt.timedelta(days=40):
                got = month_from_minutes(ins, y, m) or got   # repli : bougies 1 min du jour -> heures
                if len(got) < 300: miss += 1
            rows += got
    if rows:
        with gzip.open(f"{OUT}/{ins}_1h.csv.gz", "wt", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "o", "h", "l", "c", "v"]); w.writerows(rows)
    log.append(f"{ins} 1h: {len(rows)} bougies, {miss} échecs")
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
