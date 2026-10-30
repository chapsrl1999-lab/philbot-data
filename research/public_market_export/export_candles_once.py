#!/usr/bin/env python3
"""Only public Binance USD-M candles for isolated user research. No strategy/account data."""
import csv,hashlib,io,json,gzip,re,time,zipfile,urllib.error,urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
SWING='ALGO ATOM AVAX BTC COMP CRV DOGE DOT FET GALA HBAR ICP INJ LDO NEAR OP RUNE SOL SUI UNI XLM XRP'.split()
RECENT='1000BONK AAVE ADA ALGO APT ARB ATOM AVAX AXS BNB BTC COMP CRV DOGE DYDX ETH FET FIL FLOKI GALA HBAR ICP IMX INJ LDO LINK LTC NEAR OP ORDI PEPE PYTH RUNE SAND SEI SHIB SNX SOL STX SUI UNI VET XLM XRP'.split()
MONTHS=[(y,m) for y in [2023,2024,2025,2026] for m in range(1,13) if (y>2023 or m>=8) and (y<2026 or m<=9)]
ROOT=Path('market_only_public_candles')
BASE='https://data.binance.vision/data/futures/um/monthly/klines'
def get(url):
  for retry in range(3):
    try:
      with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Market-Data-Checksum-Study/1.0'}),timeout=25) as f:return f.read(),None
    except urllib.error.HTTPError as e:
      if e.code==404:return None,'HTTP_404'
      if retry==2:return None,'HTTP_'+str(e.code)
    except Exception as e:
      if retry==2:return None,type(e).__name__
    time.sleep(.4*(retry+1))
  return None,'unknown'
def work(job):
  s,tf,y,m=job
  fn=f'{s}-{tf}-{y}-{m:02d}.zip';url=f'{BASE}/{s}/{tf}/{fn}'
  v,err=get(url)
  if err:return job,None,{'name':fn,'error':err}
  check,err=get(url+'.CHECKSUM')
  if err:return job,None,{'name':fn,'error':'CHECKSUM_'+err}
  digest=hashlib.sha256(v).hexdigest();expected=check.decode('utf-8','replace').strip().split()[0].lower()
  if not re.fullmatch('[0-9a-f]{64}',expected) or expected!=digest:return job,None,{'name':fn,'error':'SHA256_MISMATCH'}
  try:
    with zipfile.ZipFile(io.BytesIO(v)) as z:
      names=[n for n in z.namelist() if n.endswith('.csv')]
      if len(names)!=1:raise ValueError('CSV_COUNT')
      with z.open(names[0]) as stream:raw=list(csv.reader(io.TextIOWrapper(stream,encoding='utf-8-sig')))
    rows=[]
    for a in raw:
      if not a or len(a)<5:continue
      try:
        t=int(a[0]);t=t//1000 if t>10**14 else t
        o,h,l,c=map(float,a[1:5])
        if not o>0 or not l>0 or not h>=max(o,c) or not l<=min(o,c):raise ValueError('BAD_OHLC')
        rows.append([t,o,h,l,c])
      except ValueError:
        if a[0].lower().replace('_','').replace(' ','') in ('opentime','timestamp'):continue
        raise
    if not rows:raise ValueError('NO_ROWS')
    interval=3600000 if tf=='1h' else 900000
    if any(rows[i][0]-rows[i-1][0]!=interval for i in range(1,len(rows))):raise ValueError('INTERNAL_GAP')
    return job,rows,{'name':fn,'sha256':digest,'rows':len(rows)}
  except Exception as e:return job,None,{'name':fn,'error':str(e)[:85]}
def main():
  ROOT.mkdir(exist_ok=True)
  req=[(s+'USDT','1h',y,m) for s in SWING for y,m in MONTHS]
  req += [(s+'USDT','15m',2026,9) for s in RECENT]
  data=defaultdict(list);fail=[];manifest=[]
  with ThreadPoolExecutor(max_workers=18) as ex:
    tasks=[ex.submit(work,x) for x in req]
    for n,t in enumerate(as_completed(tasks),1):
      job,rows,meta=t.result();manifest.append(meta)
      if rows is None:fail.append(meta)
      else:data[(job[0],job[1])].extend(rows)
      if n%150==0:print('download',n,'/',len(req),'missing',len(fail),flush=True)
  for tf,syms in [('1h',SWING),('15m',RECENT)]:
    out={}
    for s in syms:
      series=sorted(data.get((s+'USDT',tf),[]))
      out[s]=series
    with gzip.open(ROOT/f'candles_{tf}.json.gz','wt',encoding='utf-8',compresslevel=6) as f:json.dump(out,f,separators=(',',':'))
  meta={'verified':len(req)-len(fail),'requested':len(req),'failures':fail,'files':sorted(manifest,key=lambda d:d['name']),
        'data':'official Binance USD-M perpetual monthly 1h August2023-September2026 and 15m September2026',
        'private_strategy_code_included':False,'private_account_data_included':False}
  (ROOT/'manifest.json').write_text(json.dumps(meta,indent=2))
  print('DATA_EXPORT='+json.dumps({'verified':meta['verified'],'requested':meta['requested'],'failures':len(fail)}),flush=True)
  if len(fail)>len(req)*.12:raise SystemExit('INCOMPLETE_COVERAGE_SEE_ARTIFACT')
if __name__=='__main__':main()
