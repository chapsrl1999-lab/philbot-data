"""Actions américaines Dukascopy, 2017 → aujourd'hui, en bougies de 5 min bâties à partir des fichiers 1 min journaliers
(les fichiers horaires mensuels avaient des trous de plusieurs mois).
Reprise : si la branche de données existe déjà, seuls les jours manquants sont redemandés (un jour vide est redemandé une 2e fois, pas plus).
Limite de temps stricte : le fichier et le journal sont toujours écrits, même si tout n'a pas été demandé ; on relance pour compléter.
Format bi5 = LZMA ; enregistrements de 24 octets : temps (s, int32), open, close, low, high (int32, en millièmes), volume (float32).
Prix NON ajustés pour les fractionnements d'actions."""
import os, json, lzma, struct, time, gzip, csv, datetime as dt, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
INS = os.environ["INSTR"]; OUT = "data/duka5"; os.makedirs(OUT, exist_ok=True); BASE = "https://datafeed.dukascopy.com/datafeed"; T0 = time.time(); DEADLINE = T0 + 38 * 60
F, FS, FL = f"{OUT}/{INS}_5m.csv.gz", f"{OUT}/{INS}_jours.json", f"{OUT}/{INS}_LOG.txt"
def get(url, tries=2, timeout=12):
    for k in range(tries):
        if time.time() > DEADLINE: return None
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=timeout) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404: return b""
            time.sleep(1 + k)
        except Exception: time.sleep(1 + k)
    return None
def day(d):
    if time.time() > DEADLINE: return d, None
    raw = get(f"{BASE}/{INS}/{d.year}/{d.month - 1:02d}/{d.day:02d}/BID_candles_min_1.bi5")
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
today = dt.date.today(); days = [dt.date(2017, 1, 1) + dt.timedelta(days=k) for k in range((today - dt.date(2017, 1, 1)).days)]; days = [d for d in days if d.weekday() < 5]
state = json.load(open(FS)) if os.path.exists(FS) else {}; res = {}                       # state : date → nombre d'essais vides (0 = données présentes)
if os.path.exists(F):
    for r in csv.reader(gzip.open(F, "rt")):
        if r[0] == "t": continue
        d = dt.datetime.fromtimestamp(int(r[0]), dt.timezone.utc).date(); res.setdefault(d, []).append([int(r[0]), int(r[1]), int(r[2]), int(r[3]), int(r[4]), float(r[5])])
log = [f"{INS} : reprise avec {len(res)} jours déjà en main"]
if not res:
    probe = [d for d in days if (today - d).days <= 45][-12:]
    with ThreadPoolExecutor(6) as ex: alive = sum(1 for _, g in ex.map(day, probe) if g)
    log.append(f"sonde : {alive} jours avec données sur les 12 derniers")
else: alive = 1
if alive:
    todo = [d for d in reversed(days) if d not in res and state.get(str(d), 0) < 2]; got = vide = err = 0
    with ThreadPoolExecutor(3) as ex:
        for d, g in ex.map(day, todo):
            if g: res[d] = g; state[str(d)] = 0; got += 1
            elif g == []: state[str(d)] = state.get(str(d), 0) + 1; vide += 1
            else: err += 1
    log.append(f"cette passe : {len(todo)} jours demandés, {got} reçus, {vide} vides, {err} en erreur ou hors délai, {time.time() - T0:.0f} s")
    if res:
        with gzip.open(F, "wt", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "o", "h", "l", "c", "v"])
            for d in sorted(res): w.writerows([[r[0], r[1], r[2], r[3], r[4], round(r[5], 3)] for r in res[d]])
        json.dump(state, open(FS, "w")); first = min(res)
        for y in range(first.year, today.year + 1):
            dy = [d for d in days if d.year == y and d >= first]; miss = [d for d in dy if d not in res]
            log.append(f"{y} : {len(dy) - len(miss)} jours avec données, {sum(1 for d in miss if state.get(str(d), 0) >= 1)} vides, {sum(1 for d in miss if state.get(str(d), 0) == 0)} jamais reçus ; manquants : " + ' '.join(d.strftime('%m-%d') for d in miss))
        left = sum(1 for d in days if d >= first and d not in res and state.get(str(d), 0) < 2)
        log.append(f"total {sum(len(v) for v in res.values())} bougies 5 min, du {first} au {max(res)} ; reste à redemander : {left} jours ; {time.time() - T0:.0f} s")
open(FL, "w").write("\n".join(log) + "\n"); print("\n".join(log), flush=True)
