"""Diagnostic Dukascopy : codes de réponse et délais, en série puis en parallèle, pour comprendre les erreurs du téléchargement 5 min."""
import time, urllib.request, urllib.error, datetime as dt, os
from concurrent.futures import ThreadPoolExecutor
os.makedirs("data/diag", exist_ok=True); B = "https://datafeed.dukascopy.com/datafeed"; out = []
def one(url, ua="Mozilla/5.0"):
    t = time.time()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": ua}), timeout=20) as r: b = r.read(); return f"200 {len(b)} o {time.time()-t:.1f}s"
    except urllib.error.HTTPError as e: return f"HTTP {e.code} {time.time()-t:.1f}s"
    except Exception as e: return f"{type(e).__name__} {time.time()-t:.1f}s"
days = [dt.date(2023, 3, 1) + dt.timedelta(days=k) for k in range(60)]; days = [d for d in days if d.weekday() < 5]
u = lambda s, d: f"{B}/{s}/{d.year}/{d.month-1:02d}/{d.day:02d}/BID_candles_min_1.bi5"
out.append("--- en série, AAPL, 20 jours, pause 0,3 s"); 
for d in days[:20]: out.append(f"{d} {one(u('AAPLUSUSD', d))}"); time.sleep(.3)
out.append("--- en série, EURUSD, 8 jours")
for d in days[:8]: out.append(f"{d} {one(u('EURUSD', d))}"); time.sleep(.3)
out.append("--- fichiers horaires mensuels AAPL 2023")
for m in range(12): out.append(f"2023-{m+1:02d} {one(f'{B}/AAPLUSUSD/2023/{m:02d}/BID_candles_hour_1.bi5')}"); time.sleep(.3)
out.append("--- 5 en parallèle, MSFT, 20 jours")
with ThreadPoolExecutor(5) as ex: out += [f"{d} {r}" for d, r in zip(days[20:40], ex.map(lambda d: one(u('MSFTUSUSD', d)), days[20:40]))]
out.append("--- en série après pause de 30 s, MSFT, 10 jours"); time.sleep(30)
for d in days[:10]: out.append(f"{d} {one(u('MSFTUSUSD', d))}"); time.sleep(1)
open("data/diag/DUKA_DIAG.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
