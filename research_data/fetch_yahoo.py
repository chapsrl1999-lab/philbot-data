"""Actions américaines, source Yahoo (API publique des graphiques) : journalier depuis 2005, horaire sur 730 jours, 5 min sur 60 jours.
Prix ajustés pour les fractionnements (pas pour les dividendes). Un fichier par action et par pas de temps, plus un journal.
Variables : SHARD (0..N-1), NSHARD."""
import os, json, time, gzip, csv, urllib.request, urllib.error
OUT = "data/yh"; os.makedirs(OUT, exist_ok=True); SH, NS = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1)); T0 = time.time(); DEADLINE = T0 + 45 * 60
T = """SPY QQQ IWM DIA XLK XLF XLE XLV XLY XLP XLI XLU XLB XLRE XLC SMH GLD TLT
AAPL MSFT NVDA AMZN GOOGL META TSLA AMD NFLX AVGO PLTR COIN MSTR MU INTC HOOD ORCL BABA TSM UBER ARM SMCI LLY JPM BAC WMT COST V MA DIS BA NKE PYPL SHOP SNOW CRWD SOFI RIVN MARA
XOM CVX PFE KO PEP MCD ADBE CRM QCOM TXN ASML IBM GS UNH JNJ F GM BRK-B DELL PANW NOW ABNB DKNG RBLX NET DDOG ZM XYZ PDD JD NVO GME AMC CSCO T VZ HD LOW CAT GE MRK ABBV TMO C WFC MS AXP SBUX BKNG
AMAT LRCX MRVL ADI ROKU SNAP PINS LYFT SPOT TGT CVS UPS FDX LMT RTX DE MMM HON PG CL MO PM BMY GILD AMGN MRNA REGN ISRG
ABT ACN ADP ADSK AIG ALGN AMT ANET APD APH APP AZO BDX BIIB BK BLK BSX BX CB CDNS CEG CHTR CI CMCSA CME CMG COF COP CPRT CRSP CSX CTAS CVNA DAL DASH DHI DHR DLTR DOCU DUK DXCM EA EBAY EL ELV EMR ENPH EOG EQIX ETN ETSY EW EXPE FCX FI FSLR FTNT GD GEV GLW HAL HCA HLT HPQ HUM ICE IDXX ILMN INTU ITW KHC KKR KLAC KMB KR LEN LIN LULU LUV LVS LYV MAR MCHP MCK MCO MDLZ MDT MELI MET MMC MNST MPC MRNA MSCI MSI NEE NEM NOC NSC NTES NUE NXPI ODFL OKTA ON ORLY OXY PCAR PGR PH PLD PNC PSX PWR RCL RIOT ROST RSG SCHW SE SHW SLB SNPS SO SPG SPGI STZ SYK SYY TEAM TJX TMUS TRV TSCO TT TTD TTWO TWLO U UAL ULTA UNP URI USB VLO VRTX VST WBA WBD WDAY WDC WM WMB WYNN ZS ZTS
AFRM AI ASTS BIDU BILI CCL CELH CHWY CLSK COHR DJT DOCS DUOL ENPH FUBO HIMS IONQ LCID LI MDB MRNA NCLH NIO OKLO OPEN PATH PENN PTON QS RDDT RGTI RKLB S SOUN TOST UPST VKTX W XPEV ZIM""".split()
T = list(dict.fromkeys(T)); mine = [t for i, t in enumerate(T) if i % NS == SH]
def get(sym, interval, rng):
    for k in range(5):
        if time.time() > DEADLINE: return None, 'délai'
        host = ('query1', 'query2')[k % 2]
        url = f"https://{host}.finance.yahoo.com/v8/finance/chart/{sym}?interval={interval}&{rng}&includePrePost=false&events=split"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", "Accept": "application/json"}), timeout=30) as r:
                return json.loads(r.read()), 'ok'
        except urllib.error.HTTPError as e:
            if e.code == 404: return None, '404'
            last = f'HTTP {e.code}'; time.sleep(3 * (k + 1))
        except Exception as e: last = type(e).__name__; time.sleep(3 * (k + 1))
    return None, last
log = []
for sym in mine:
    line = [sym]
    for interval, rng, tag in (('1d', 'period1=1104537600&period2=9999999999', '1d'), ('1h', 'range=730d', '1h'), ('5m', 'range=60d', '5m')):
        j, st = get(sym, interval, rng); n = 0
        try:
            if j:
                r = j['chart']['result'][0]; ts = r.get('timestamp') or []; q = r['indicators']['quote'][0]
                rows = [[t, q['open'][i], q['high'][i], q['low'][i], q['close'][i], q['volume'][i]] for i, t in enumerate(ts) if q['close'][i] is not None and q['open'][i] is not None]
                n = len(rows)
                if rows:
                    with gzip.open(f"{OUT}/{sym}_{tag}.csv.gz", "wt", newline="") as f:
                        w = csv.writer(f); w.writerow(["t", "o", "h", "l", "c", "v"]); w.writerows([[x[0]] + [round(v, 4) for v in x[1:5]] + [x[5] or 0] for x in rows])
                sp = (r.get('events') or {}).get('splits') or {}
                if tag == '1d' and sp: line.append('fractionnements ' + ' '.join(f"{time.strftime('%Y-%m-%d', time.gmtime(v['date']))}:{v['splitRatio']}" for v in sp.values()))
        except Exception as e: st = 'lecture ' + type(e).__name__
        line.append(f"{tag} {st} {n}"); time.sleep(0.6)
    log.append(' | '.join(line)); print(log[-1], flush=True)
open(f"{OUT}/LOG_{SH}.txt", "w").write("\n".join(log) + f"\n{time.time() - T0:.0f} s\n")
