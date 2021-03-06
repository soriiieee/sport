# https://api.rakuten.net/api-sports/api/api-football?endpoint=apiendpoint_33b2c650-e8fb-4ac6-aa3c-715d2bb5032f
# reference

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
    list_res = text.split(",")
  else:
    text =re.sub("勝",",",text)
    text = re.sub("敗","",text)
    # text = text+"0"
    list_res = text.split(",") + ["0"]
  
  # print(len(list_res), "-", list_res)
  return list_res

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
        # print(c)
        # sys.exit()
        if c is None:
          c="nan"
        for _ in range(len(r.find_all("em"))):
          _c.append(c.text)
          # print(c), sys.exit()
        for j, e in enumerate(r.find_all("em")):
          # print(c,j,e)
          # print(e), sys.exit()
          _n.append(e.text)
        
        # sys.exit()
        for j, e in enumerate(r.find_all("span",class_="yjMS ml5p")):
          # print(e.text)
          list_result = convert_res(e.text)
          if len(list_result) == 3:
            _w.append(list_result[0])
            _l.append(list_result[1])
            _r.append(list_result[2])
          else:
            _w.append(9999)
            _l.append(9999)
            _r.append(9999)
    
    # sys.exit()
  
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

def making_concat_data(_season, out_path):
  _df = []
  for season in _season:
    input_path = f"{outd}/result_{season}.csv"
    if os.path.exists(input_path):
      df = pd.read_csv(input_path)
      # print(df.head())
      _df.append(df)

  df = pd.concat(_df, axis=0)
  df.to_csv(out_path, index=False)
  return
  
def mk_ban_point(x):
  for c in ["筆頭"] + [str(i) for i in range(2, 20)]:
    if c in x:
      if c == "筆頭":
        return 20-1
      else:
        return 20 - int(c)
    else:
      pass
  return

def make_rank_point(x):
  if "横綱" in x:
    return 300
  if "大関" in x:
    return 150
  if '関脇' in x:
    return 100
  if '小結' in x:
    return 80
  if "前頭" in x:
    return 50 + mk_ban_point(x)
  if "十両" in x:
    return 20 + mk_ban_point(x)

def make_basho_point(x):
  n_win = x[0]
  n_lose = x[1]
  n_pose = x[2]
  # make day point---
  day_point = 3 * n_win + 0 * n_lose
  # make katikoshi point---
  if n_win >= 8:
    day_point += 10
  if n_lose >= 8:
    day_point += -10
  # make pose points---
  day_point += - 3 * n_pose
  return day_point


if __name__ == "__main__":
  datd ='../dat/sumou'
  outd = '../out/sumou'
  outd2 = '../out/sumou2'
  
  os.makedirs(outd2, exist_ok=True)
  # os.makedirs(datd, exist_ok=True)

  # subprocess.run('rm -f *.png', cwd=outd, shell=True)

  _season = [f"{yy}{str(ii).zfill(2)}" for yy in [2016, 2017, 2018, 2019, 2020] for ii in np.arange(1, 12, 2)]
  out_5y_path = f"{outd2}/sumou_results5y_0.csv"

  #--------------------------------------------------------
  # analysis datas ...-------------------
  df = pd.read_csv(out_5y_path)
  print(df["ban"].unique())
  print(df["ban"] == '横綱大関')
  df["rank_point"] = df["ban"].apply(lambda x: make_rank_point(x))
  df["day_point"] = df["win"].apply(lambda x: 3 * x)
  df["all_point"] = df[["win", "lose", "pose"]].apply(lambda x: make_basho_point(x), axis=1)
  
  df.to_csv(f"{outd2}/sumou_results5y_1.csv",index=False)
  print(df.head())
  sys.exit()

  #--------------------------------------------------------
  # concat datas ...-------------------
  # making_concat_data(_season, out_path)
  # sys.exit()

  #--------------------------------------------------------
  # get infomation ...-------------------
  # try:
  #   get_sumou_result(season=season, out_csv=out_csv)
  # except:
  #   pass
  #--------------------------------------

  # print(df.head())
  sys.exit()
  
  
  print("start sumou_model...")

