#!/usr/bin/env python3
"""Official public USD-M futures daily 1h October 1–28 2026; prices only."""
import csv,gzip,hashlib,io,json,zipfile,urllib.request,re,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from collections import defaultdict
from pathlib import Path
SYMS='ALGO ATOM AVAX BTC COMP CRV DOGE DOT FET GALA HBAR ICP INJ LDO NEAR OP RUNE SOL SUI UNI XLM XRP'.split()
ROOT=Path('public_oct_1h');ROOT.mkdir(exist_ok=True)
def download(job):
 s,d=job;name=f'{s}USDT-1h-2026-10-{d:02d}.zip'
 u='https://data.binance.vision/data/futures/um/daily/klines/'+s+'USDT/1h/'+name
 for it in range(3):
  try:
   b=urllib.request.urlopen(u,timeout=25).read()
   c=urllib.request.urlopen(u+'.CHECKSUM',timeout=25).read().decode().split()[0]
   h=hashlib.sha256(b).hexdigest()
   if c!=h or not re.fullmatch('[a-f0-9]{64}',c):raise ValueError('SHA256 mismatch')
   with zipfile.ZipFile(io.BytesIO(b)) as z:
    csvs=[x for x in z.namelist() if x.endswith('.csv')]
    if len(csvs)!=1:raise ValueError('CSV COUNT')
    with z.open(csvs[0]) as f:rr=list(csv.reader(io.TextIOWrapper(f,encoding='utf-8-sig')))
   rows=[]
   for a in rr:
    if len(a)<5:continue
    try:
     t=int(a[0]);t=t//1000 if t>10**14 else t
     o,hi,lo,cl=map(float,a[1:5])
     if not(o>0 and lo>0 and hi>=max(o,cl) and lo<=min(o,cl)):raise ValueError('OHLC')
     rows.append([t,o,hi,lo,cl])
    except ValueError:
     if a[0].lower().replace('_','')=='opentime':continue
     raise
   if len(rows)!=24 or any(rows[i][0]-rows[i-1][0]!=3600000 for i in range(1,len(rows))):raise ValueError('GAP')
   return s,rows,{'name':name,'sha256':h,'rows':24}
  except Exception as e:
   if it==2:return s,None,{'name':name,'error':type(e).__name__+':'+str(e)[:120]}
   time.sleep(.3*(it+1))
data=defaultdict(list);metadata=[];bad=[]
req=[(s,d) for s in SYMS for d in range(1,29)]
with ThreadPoolExecutor(max_workers=18) as pool:
 for n,f in enumerate(as_completed([pool.submit(download,x) for x in req]),1):
  s,arr,m=f.result();metadata.append(m)
  if arr:data[s].extend(arr)
  else:bad.append(m)
  if n%120==0:print('oct_daily_verified',n,'/',len(req),'errors',len(bad),flush=True)
for s in data:data[s].sort()
with gzip.open(ROOT/'oct_1h.json.gz','wt') as f:json.dump(data,f,separators=(',',':'))
(ROOT/'manifest.json').write_text(json.dumps({'requested':len(req),'verified':len(req)-len(bad),'failures':bad,'archive_sha256':metadata,'coverage':'October 1-28 UTC only, no October29 partial'},indent=2))
print('OCT_PUBLIC_MARKET_DONE',len(req)-len(bad),'/',len(req))
if bad:raise SystemExit('EXPLICIT_MISSING_DAILY_FILES')
