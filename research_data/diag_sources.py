"""Diagnostic des sources de données d'actions depuis un serveur GitHub : Yahoo, Stooq, Nasdaq. Codes de réponse, taille, premières lignes."""
import time, urllib.request, urllib.error, os, json
os.makedirs("data/diag", exist_ok=True); out = []
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
def one(name, url, headers=None):
    t = time.time(); h = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"}; h.update(headers or {})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r: b = r.read(); out.append(f"{name} : 200, {len(b)} o, {time.time()-t:.1f}s | {b[:160]!r}")
    except urllib.error.HTTPError as e: out.append(f"{name} : HTTP {e.code} {time.time()-t:.1f}s | {e.read()[:120]!r}")
    except Exception as e: out.append(f"{name} : {type(e).__name__} {time.time()-t:.1f}s")
for s in ("AAPL", "NVDA", "KO"):
    one(f"yahoo 1d {s}", f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?interval=1d&range=5d"); time.sleep(1)
    one(f"yahoo2 1d {s}", f"https://query2.finance.yahoo.com/v8/finance/chart/{s}?interval=1d&period1=1104537600&period2=9999999999"); time.sleep(1)
    one(f"yahoo 1h {s}", f"https://query2.finance.yahoo.com/v8/finance/chart/{s}?interval=1h&range=730d"); time.sleep(1)
    one(f"stooq 1d {s}", f"https://stooq.com/q/d/l/?s={s.lower()}.us&i=d"); time.sleep(1)
    one(f"stooq 1h {s}", f"https://stooq.com/q/d/l/?s={s.lower()}.us&i=60"); time.sleep(1)
    one(f"stooq 5m {s}", f"https://stooq.com/q/d/l/?s={s.lower()}.us&i=5"); time.sleep(1)
    one(f"nasdaq 1d {s}", f"https://api.nasdaq.com/api/quote/{s}/historical?assetclass=stocks&fromdate=2016-01-01&todate=2026-11-11&limit=9999", {"Origin": "https://www.nasdaq.com", "Referer": "https://www.nasdaq.com/"}); time.sleep(1)
    one(f"nasdaq earnings {s}", f"https://api.nasdaq.com/api/company/{s}/earnings-surprise", {"Origin": "https://www.nasdaq.com", "Referer": "https://www.nasdaq.com/"}); time.sleep(1)
one("nasdaq calendrier résultats", "https://api.nasdaq.com/api/calendar/earnings?date=2026-10-29", {"Origin": "https://www.nasdaq.com", "Referer": "https://www.nasdaq.com/"})
one("stooq db", "https://stooq.com/db/h/")
one("binance vision", "https://data.binance.vision/data/futures/um/monthly/klines/TSLAUSDT/5m/TSLAUSDT-5m-2026-08.zip")
open("data/diag/SOURCES.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
