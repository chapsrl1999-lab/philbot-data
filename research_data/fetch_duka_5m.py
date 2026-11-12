"""Actions américaines Dukascopy, 2017 → aujourd'hui, en bougies de 5 min bâties à partir des fichiers 1 min journaliers
(les fichiers horaires mensuels avaient des trous de plusieurs mois). Chaque jour ouvrable vide est redemandé deux fois,
plus lentement ; le journal compte les jours ouvrables restés vides par année (≈ 9 à 10 jours fériés attendus).
Format bi5 = LZMA ; enregistrements de 24 octets : temps (s, int32), open, close, low, high (int32, en millièmes), volume (float32).
Prix NON ajustés pour les fractionnements d'actions."""
import os, sys, lzma, struct, time, gzip, csv, datetime as dt, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
INS = os.environ["INSTR"]; OUT = "data/duka5"; os.makedirs(OUT, exist_ok=True); BASE = "https://datafeed.dukascopy.com/datafeed"; T0 = time.time(); DEADLINE = T0 + 45 * 60
def get(url, tries=4, pause=1.5):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404: return b""
            time.sleep(pause * (k + 1))
        except Exception: time.sleep(pause * (k + 1))
    return None
def day(d, tries=4, pause=1.5):
    raw = get(f"{BASE}/{INS}/{d.year}/{d.month - 1:02d}/{d.day:02d}/BID_candles_min_1.bi5", tries, pause)
    if raw is None: return d, None
    if not raw: return d, []
    try: data = lzma.decompress(raw)
    except Exception: return d, None
    t0 = int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp()); bars = {}
    for i in range(0, len(data) - 23, 24):
        s, o, c, l, h, v = struct.unpack(">iiiiif", data[i:i + 24])
        if v <= 0: continue
        k = t0 + s - s % 300; b = bars.get(k)
        if b is None: bars[k] = [k, o, h, l, c, v]
        else: b[2] = max(b[2], h); b[3] = min(b[3], l); b[4] = c; b[5] += v
    return d, [bars[k] for k in sorted(bars)]
today = dt.date.today(); probe = [today - dt.timedelta(days=k) for k in range(3, 40)]
with ThreadPoolExecutor(4) as ex: alive = sum(1 for _, g in ex.map(day, probe) if g)
log = [f"{INS} : {alive} jours avec données sur les 37 derniers"]
if alive:
    days = [dt.date(2017, 1, 1) + dt.timedelta(days=k) for k in range((today - dt.date(2017, 1, 1)).days)]; days = [d for d in days if d.weekday() < 5]
    res = {}
    with ThreadPoolExecutor(6) as ex:
        for d, g in ex.map(day, days): res[d] = g
    for rnd, (th, pause) in enumerate(((3, 3.0), (2, 5.0))):          # deuxième et troisième passes, plus lentes, sur les jours vides ou en erreur
        todo = [d for d in days if not res[d]]; first = min((d for d in days if res[d]), default=None)
        todo = [d for d in todo if first and d > first]
        if not todo or time.time() > DEADLINE: break
        got = 0
        with ThreadPoolExecutor(th) as ex:
            for d, g in ex.map(lambda d: day(d, 5, pause), todo):
                if g: got += 1; res[d] = g
                elif g is None and res[d] is not None: res[d] = None
        log.append(f"passe {rnd + 2} : {len(todo)} jours redemandés, {got} récupérés, {time.time() - T0:.0f} s")
    rows = [r for d in days for r in (res[d] or [])]
    if rows:
        with gzip.open(f"{OUT}/{INS}_5m.csv.gz", "wt", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "o", "h", "l", "c", "v"]); w.writerows([[r[0], r[1], r[2], r[3], r[4], round(r[5], 3)] for r in rows])
        first = min(d for d in days if res[d])
        for y in range(first.year, today.year + 1):
            dy = [d for d in days if d.year == y and d >= first]
            log.append(f"{y} : {sum(1 for d in dy if res[d])} jours avec données, {sum(1 for d in dy if res[d] == [])} vides, {sum(1 for d in dy if res[d] is None)} en erreur ; vides/erreurs : " + ' '.join(d.strftime('%m-%d') for d in dy if not res[d]))
        log.append(f"total {len(rows)} bougies 5 min, du {first} au {max(d for d in days if res[d])}, {time.time() - T0:.0f} s")
open(f"{OUT}/{INS}_LOG.txt", "w").write("\n".join(log) + "\n"); print("\n".join(log), flush=True)
