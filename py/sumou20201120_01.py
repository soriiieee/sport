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

import japanize_matplotlib
# print(japanize_matplotlib.__file__)
# sys.exit()



def make_master(out_csv):
  outd ='../out/sumou'
  _file = glob.glob(f'{outd}/result_*.csv')
  _df = []
  for f_path in _file:
    df = pd.read_csv(f_path)
    _df.append(df)
  
  df = pd.concat(_df,axis=0)
  df.to_csv(out_csv, index=False)
  print("end making result master...")
  return 

if __name__ == "__main__":
  outd ='../out/sumou'
  os.makedirs(outd, exist_ok=True)
  # subprocess.run('rm -f *.png', cwd=outd, shell=True)

  #-------------------------------------------------
  out_csv = f"{outd}/master_makuuchi.csv"
  # make_master(out_csv)
  #-------------------------------------------------
  if os.path.exists(out_csv):
    df = pd.read_csv(out_csv)
  else:
    make_master(out_csv)
    df = pd.read_csv(out_csv)
  
  df["season"] = df[["year","basho"]].apply(lambda x: str(x[0])+str(x[1]).zfill(2),axis=1)
  n_basho5 = df["season"].nunique()

  _season = df["season"].unique()
  _name = df["name"].unique()
  for name in _name:
    tmp = df[df["name"]==name]
    for season in _season:
      
    print(tmp)
    sys.exit()
  tmp = df.groupby(["name","year"])["win","lose","pose"].sum()
  for name,yy in tmp.index:
    print(name,yy)
  sys.exit()
  print(df.dtypes)
  sys.exit()
  # tmp = df.groupby("name").count().sort_values(["season","ban"],ascending=False)

  tmp = tmp.reset_index()
  print(tmp)
  sys.exit()


  _season=[ f"{yy}{str(ii).zfill(2)}" for yy in [2016,2017,2018,2019,2020] for ii in np.arange(1,12,2)]


  
  
  print("start sumou_model...")

