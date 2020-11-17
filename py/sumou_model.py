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

import requests
from bs4 import BeautifulSoup


def get_sumou_result(season, out_csv):
  if os.path.exists(out_csv):
    return pd.read_csv(out_csv)
  url = f"https://sports.yahoo.co.jp/sumo/torikumi/hoshitori/?bashoId={season}"
  
  if os.path.exists(f"../dat/sumou/result_{season}.dat"):
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
  _n0, _n1, _r0, _r1 = [], [], [], []
  _c0, _c1 = [], []
  
  for i, r in enumerate(soup.find("tbody").find_all("tr"))):
    if i % 2 == 0:
      c = r.find("td", class_="banduke_td")
      
      #name add list-----------------------
      for j, e in enumerate(r.find_all("em")):
        if j % 2 == 0:
          _n0.append(e.text)
          if c is None:
            _c1.append("nan")
          else:
            _c1.append(c.text)
        else:
          _n1.append(e.text)
          if c is None:
            _c1.append("nan")
          else:
            _c1.append(c.text)
            
      #name add list-----------------------      
      for j, e in enumerate(r.find_all("em")):

      sys.exit()
  return
if __name__ == "__main__":
  out_csv = f"../out/sumou/result_{season}.csv"
  df = get_sumou_result(season="202011", out_csv=out_csv)
  
  
  print("start sumou_model...")

