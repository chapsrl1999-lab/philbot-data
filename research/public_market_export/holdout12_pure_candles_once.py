#!/usr/bin/env python3
"""Only official public Binance futures candles for 12 pre-registered new assets; no private strategy or account data."""
import urllib.request,urllib.error,hashlib,csv,io,zipfile,gzip,json,time,re
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
ASSETS='AAVE ADA APE BCH BNB ETH FIL LINK LTC SAND VET ZEC'.split()
MONTHS=[(y,m) for y in [2023,2024,2025,2026] for m in range(1,13) if (y>2023 or m>=8) and (y<2026 or m<=9)]
ROOT=Path('holdout12_public_ohlcv');ROOT.mkdir(exist_ok=True)
BASE='https://data.binance.vision/data/futures/um'
H=3600000
def fetch(url):
 for i in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PhilBot-Study-Only-VerifiedPublicOHLC/20261029'}),timeout=25) as f:return f.read(),None
  except urllib.error.HTTPError as e:
   if e.code==404:return None,'HTTP404'
   if i==2:return None,'HTTP'+str(e.code)
  except Exception as e:
   if i==2:return None,type(e).__name__
  time.sleep(.5*(i+1))
 return None,'UNKNOWN'
def one(job):
 sym,year,period=job
 name=f'{sym}USDT-1h-{period}.zip'
 if year=='monthly':url=f'{BASE}/monthly/klines/{sym}USDT/1h/{name}'
 else:url=f'{BASE}/daily/klines/{sym}USDT/1h/{name}'
 data,err=fetch(url)
 if err:return job,None,{'name':name,'error':err}
 ck,err=fetch(url+'.CHECKSUM')
 if err:return job,None,{'name':name,'error':'CHECKSUM_'+err}
 sha=hashlib.sha256(data).hexdigest();expected=ck.decode('utf-8','replace').strip().split()[0].lower()
 if not re.fullmatch(r'[0-9a-f]{64}',expected) or sha!=expected:return job,None,{'name':name,'error':'SHA256_MISMATCH'}
 try:
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   filenames=[x for x in z.namelist() if x.endswith('.csv')]
   if len(filenames)!=1:raise ValueError('ZIP_MEMBER_COUNT')
   with z.open(filenames[0]) as f:rr=list(csv.reader(io.TextIOWrapper(f,encoding='utf-8-sig')))
  bars=[]
  for r in rr:
   if len(r)<5:continue
   try:
    t=int(r[0]);t=t//1000 if t>10**14 else t
    o,hi,lo,cl=map(float,r[1:5])
    if not(o>0 and lo>0 and hi>=max(o,cl) and lo<=min(o,cl)):raise ValueError('BAD_OHLC')
    bars.append([t,o,hi,lo,cl])
   except ValueError:
    if r[0].lower().replace('_','') in ('opentime','timestamp'):continue
    raise
  if len(bars)<20 or any(bars[i][0]-bars[i-1][0]!=H for i in range(1,len(bars))):raise ValueError('BARS_GAP')
  return job,bars,{'name':name,'sha256':sha,'n':len(bars)}
 except Exception as e:return job,None,{'name':name,'error':type(e).__name__+':'+str(e)[:85]}
def main():
 jobs=[(s,'monthly',f'{y}-{m:02d}') for s in ASSETS for y,m in MONTHS]
 jobs += [(s,'daily',f'2026-10-{d:02d}') for s in ASSETS for d in range(1,28)]
 out=defaultdict(list);manifest=[];fails=[]
 with ThreadPoolExecutor(max_workers=20) as p:
  fut=[p.submit(one,j) for j in jobs]
  for i,f in enumerate(as_completed(fut),1):
   job,bars,d=f.result();manifest.append(d)
   if bars is None:fails.append(d)
   else:out[job[0]].extend(bars)
   if i%180==0:print('HOLDOUT12_DOWNLOAD',i,'of',len(jobs),'fails',len(fails),flush=True)
 cont={}
 for s in ASSETS:
  arr=sorted(out[s],key=lambda x:x[0])
  gaps=sum(arr[i][0]-arr[i-1][0]!=H for i in range(1,len(arr)))
  cont[s]={'n':len(arr),'first':arr[0][0] if arr else None,'last':arr[-1][0] if arr else None,'gaps':gaps}
  out[s]=arr
 with gzip.open(ROOT/'holdout12_prices_1h.json.gz','wt',encoding='utf-8',compresslevel=6) as g:json.dump(out,g,separators=(',',':'))
 (ROOT/'manifest.json').write_text(json.dumps({'requested':len(jobs),'verified':len(jobs)-len(fails),'failures':fails,'archive_checksums':sorted(manifest,key=lambda x:x['name']),'coverage':cont,'only_public_market_data':True,'private_strategy_included':False},indent=2))
 print('HOLDOUT12_FINAL',len(jobs)-len(fails),'/',len(jobs),str(cont),flush=True)
 if fails:raise SystemExit('INCOMPLETE_OFFICIAL_ARCHIVES')
if __name__=='__main__':main()
