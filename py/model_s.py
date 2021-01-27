import numpy as np
import sys, os, re, glob
# sys.path.append('/Users/soriiieee/.local/lib/python3.7/site-packages')
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from datetime import datetime, timedelta

import requests
import json
import warnings
warnings.simplefilter("ignore")
import time
import requests
try:
  from bs4 import BeautifulSoup
except:
  from beautifulsoup4 import BeautifulSoup


def convert_res(text):
  if "休" in text:
    text =re.sub("勝",",",text)
    text = re.sub("敗",",",text)
    text = re.sub("休","",text)
    return text.split(",")
  else:
    text =re.sub("勝",",",text)
    text = re.sub("敗","",text)
    # text = text+"0"
    return text.split(",")+["0"]

def get_sumou_result(season, out_csv):
  if os.path.exists(out_csv):
    print(f"[Already] get-csv - {season} ")
    return
  # url = f"https://sports.yahoo.co.jp/sumo/torikumi/hoshitori/?bashoId={season}"
  url = f"https://sports.yahoo.co.jp/sumo/torikumi/hoshitori/?bashoId={season}#h_jyuryo"
  if os.path.exists(f"../dat/sumou/result_{season}.dat"):
    print(f"[Already] get-dat - {season} [Now] make datasets...")
    with open(f"../dat/sumou/result_{season}.dat", "r") as f:
      data = f.read()
  else:
    r = requests.get(url)
    if r.status_code == 200:
      print(f"Got OK {season}")
      with open(f"../dat/sumou/result_{season}.dat", "w") as f:
        f.write(r.text)
      data = r.text
    else:
      print("Not data...")
  soup = BeautifulSoup(data, "html")
  _n,_c =[],[]
  _w,_l,_r=[],[],[]
  
  for n in range(2):
    if n == 0: print("makuuchi result...")
    if n == 1: print("juryou result...")
    for i, r in enumerate(soup.find_all("tbody")[n].find_all("tr")):
      # i==2
      if i % 2 == 0:
        c = r.find("td", class_="banduke_td")
        if c is None:
          c="nan"
        for _ in range(len(r.find_all("em"))):
          _c.append(c.text)
          # print(c), sys.exit()
        for j, e in enumerate(r.find_all("em")):
          _n.append(e.text)
        for j, e in enumerate(r.find_all("span",class_="yjMS ml5p")):
          # print(e.text)
          w,l,r = convert_res(e.text)
          # print(w,l,r)
          _w.append(w)
          _l.append(l)
          _r.append(r)
  
  df=pd.DataFrame()
  df["name"] = _n
  df["ban"] = _c
  df["win"] = _w
  df["lose"] = _l
  df["pose"] = _r
  df["year"] = str(season)[:4]
  df["basho"] = str(season)[4:6]

  df.to_csv(out_csv,index=False)
  return


if __name__ == "__main__":
  datd ='../dat/sumou'
  outd ='../out/sumou'
  os.makedirs(outd, exist_ok=True)
  os.makedirs(datd, exist_ok=True)

  # subprocess.run('rm -f *.png', cwd=outd, shell=True)

  _season=[ f"{yy}{str(ii).zfill(2)}" for yy in [2016,2017,2018,2019,2020] for ii in np.arange(1,12,2)]
  for season in _season:
    out_csv = f"../out/sumou/result_{season}.csv"
    get_sumou_result(season=season, out_csv=out_csv)
    
    sys.exit()
    #--------------------------------------------------------
    # get infomation ...-------------------
    # try:
    #   get_sumou_result(season=season, out_csv=out_csv)
    # except:
    #   pass
    #--------------------------------------
    # 

  # print(df.head())
  sys.exit()
  
  
  print("start sumou_model...")

