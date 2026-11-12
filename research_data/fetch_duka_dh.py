"""Actions américaines Dukascopy : bougies JOURNALIÈRES (un fichier par année) et HORAIRES (un fichier par mois), 2015 → aujourd'hui.
Peu de fichiers par action (≈ 155), donc on peut insister poliment : jusqu'à 6 essais espacés par fichier, 2 fichiers à la fois.
Reprise : les fichiers déjà reçus (branche de données) ne sont pas redemandés. Journal par action : fichiers reçus, vides, en erreur.
Format bi5 = LZMA ; 24 octets par bougie : temps (s depuis le début du fichier, int32), open, close, low, high (int32, millièmes), volume (float32).
Prix NON ajustés pour les fractionnements. Variables : SHARD, NSHARD."""
import os, json, lzma, struct, time, gzip, csv, random, datetime as dt, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
OUT = "data/dh"; os.makedirs(OUT, exist_ok=True); BASE = "https://datafeed.dukascopy.com/datafeed"; T0 = time.time(); DEADLINE = T0 + 42 * 60
SH, NS = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
T = """AAPL MSFT NVDA AMZN GOOGL TSLA AMD NFLX AVGO PLTR MU INTC HOOD ORCL BABA TSM UBER ARM SMCI LLY JPM BAC WMT COST V MA DIS BA NKE PYPL SHOP SNOW CRWD SOFI RIVN MARA
XOM CVX PFE KO PEP MCD ADBE CRM QCOM TXN ASML IBM GS UNH JNJ F GM DELL PANW NOW ABNB DKNG RBLX NET DDOG ZM SQ PDD JD NVO GME AMC CSCO T VZ HD LOW CAT GE MRK ABBV TMO C WFC MS AXP SBUX BKNG
AMAT LRCX MRVL ADI ROKU SNAP PINS LYFT SPOT TGT CVS UPS FDX LMT RTX DE MMM HON PG CL MO PM BMY GILD AMGN MRNA REGN ISRG CRCL APP RDDT
ABT ACN ADP ADSK AIG ALGN AMT ANET APD BDX BIIB BK BLK BSX BX CB CDNS CHTR CI CMCSA CME CMG COF COP CSX DAL DHI DHR DLTR DOCU DUK EA EBAY EL EMR ENPH EOG EQIX ETN ETSY EW EXPE FCX FSLR FTNT GD GLW HAL HCA HLT HPQ HUM ICE IDXX ILMN INTU ITW KHC KKR KLAC KMB KR LEN LIN LULU LUV LVS MAR MCHP MCK MCO MDLZ MDT MELI MET MMC MNST MPC MSCI NEE NEM NOC NSC NTES NUE NXPI OKTA ON ORLY OXY PCAR PGR PH PLD PNC PSX RCL RIOT ROST SCHW SE SHW SLB SNPS SO SPG SPGI STZ SYK SYY TEAM TJX TMUS TRV TTD TTWO TWLO U UAL ULTA UNP URI USB VLO VRTX WBA WBD WDAY WDC WM WMB WYNN ZS ZTS
AFRM BIDU BILI CCL CHWY CVNA DASH LCID LI NCLH NIO PTON UPST W XPEV""".split()
T = list(dict.fromkeys(T)); mine = [t for i, t in enumerate(T) if i % NS == SH]
def get(url, tries=6):
    for k in range(tries):
        if time.time() > DEADLINE: return None
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=20) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404: return b""
        except Exception: pass
        time.sleep(2 + 2 * k + random.random() * 2)
    return None
def parse(raw, t0):
    data = lzma.decompress(raw); out = []
    for i in range(0, len(data) - 23, 24):
        s, o, c, l, h, v = struct.unpack(">iiiiif", data[i:i + 24])
        if v > 0: out.append([t0 + s, o, h, l, c, round(v, 4)])
    return out
now = dt.datetime.utcnow(); cur = (now.year, now.month - 1)
# Ordre : d'abord les fichiers journaliers de toutes les actions du lot (12 par action), puis les fichiers horaires, du mois le plus récent au plus ancien,
# en tournant sur les actions. Tout est écrit à la fin (limite de temps stricte), et la passe suivante reprend ce qui manque.
ST, DATA, CNT = {}, {}, {}
for sym in mine:
    fs = f"{OUT}/{sym}_etat.json"; ST[sym] = json.load(open(fs)) if os.path.exists(fs) else {}; DATA[sym] = {"d": {}, "h": {}}; CNT[sym] = [0, 0, 0]
    for tag in ("d", "h"):
        f = f"{OUT}/{sym}_1{tag}.csv.gz"
        if os.path.exists(f):
            for r in csv.reader(gzip.open(f, "rt")):
                if r[0] != "t": DATA[sym][tag][int(r[0])] = r
todo = lambda sym, key: ST[sym].get(key, "") not in ("ok", "vide2")
def one(j):
    sym, tag, y, m = j; ins = sym + "USUSD"
    url = f"{BASE}/{ins}/{y}/BID_candles_day_1.bi5" if tag == "d" else f"{BASE}/{ins}/{y}/{m:02d}/BID_candles_hour_1.bi5"
    raw = get(url, 4); t0 = int(dt.datetime(y, 1 if tag == "d" else m + 1, 1, tzinfo=dt.timezone.utc).timestamp())
    if raw is None: return j, None
    if not raw: return j, []
    try: return j, parse(raw, t0)
    except Exception: return j, None
def run(jobs):
    for a0 in range(0, len(jobs), 12):
        if time.time() > DEADLINE: return
        with ThreadPoolExecutor(3) as ex:
            for (sym, tag, y, m), g in ex.map(one, jobs[a0:a0 + 12]):
                key = f"{tag}{y}-{m}"
                if g:
                    for r in g: DATA[sym][tag][r[0]] = r
                    CNT[sym][0] += 1
                    if not ((tag == "d" and y == now.year) or (tag == "h" and (y, m) == cur)): ST[sym][key] = "ok"
                elif g == []: ST[sym][key] = "vide2" if ST[sym].get(key) == "vide" else "vide"; CNT[sym][1] += 1
                else: CNT[sym][2] += 1
run([(sym, "d", y, None) for y in range(now.year, 2014, -1) for sym in mine if todo(sym, f"d{y}-None")])
alive = [sym for sym in mine if DATA[sym]["d"] or DATA[sym]["h"] or not any(ST[sym].get(f"d{y}-None", "").startswith("vide") for y in (now.year, now.year - 1, now.year - 2))]
run([(sym, "h", y, m) for y in range(now.year, 2014, -1) for m in range(11, -1, -1) if dt.datetime(y, m + 1, 1) <= now for sym in alive if todo(sym, f"h{y}-{m}") and not ST[sym].get(f"d{y}-None", "").startswith("vide")])
logs = []
for sym in mine:
    for tag in ("d", "h"):
        if DATA[sym][tag]:
            with gzip.open(f"{OUT}/{sym}_1{tag}.csv.gz", "wt", newline="") as f:
                w = csv.writer(f); w.writerow(["t", "o", "h", "l", "c", "v"]); w.writerows([DATA[sym][tag][k] for k in sorted(DATA[sym][tag], key=int)])
    json.dump(ST[sym], open(f"{OUT}/{sym}_etat.json", "w"))
    okd = sum(1 for k, v in ST[sym].items() if k[0] == "d" and v == "ok"); okh = sum(1 for k, v in ST[sym].items() if k[0] == "h" and v == "ok")
    logs.append(f"{sym} : cette passe {CNT[sym][0]} reçus, {CNT[sym][1]} vides, {CNT[sym][2]} en erreur ; en main {len(DATA[sym]['d'])} jours ({okd} années finies), {len(DATA[sym]['h'])} heures ({okh} mois finis){'' if sym in alive else ' ; absente chez Dukascopy ?'}")
open(f"{OUT}/LOG_{SH}.txt", "w").write("\n".join(logs) + f"\n{time.time() - T0:.0f} s\n"); print("\n".join(logs), flush=True)
