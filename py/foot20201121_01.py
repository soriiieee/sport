
# https://api.rakuten.net/api-sports/api/api-football?endpoint=apiendpoint_33b2c650-e8fb-4ac6-aa3c-715d2bb5032f
# reference

import numpy as np
import sys, os, re, glob
# sys.path.append("./")
# print(sys.path)
# sys.exit()
import re
# sys.path.append('/Users/soriiieee/.local/lib/python3.7/site-packages')
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

import requests
import json

#sori making Class...
from model_f import GetFootballLeagueInfo
from model_f import get_team_statics #(season=2019, team=298, league=283):
from model_f import plot_pie #(ax, df, col)

def load_json(json_path):
  with open(json_path, "r") as json_file:
    json_data = json.load(json_file)
  return json_data

def load_league(code):
  if os.path.exists(f"../dat/football/init_{code}.csv"):
    print("already set up...")
    df = pd.read_csv(f"../dat/football/init_{code}.csv")
    return df
  else:
    print("set up Now...")
    json_path = f"../dat/football/init_json_{code}.json"
    jf = load_json(json_path)
    df = pd.DataFrame(jf["api"]["leagues"])
    df = df[["league_id","name","season"]].sort_values("season", ascending=False)
    df.to_csv(f"../dat/football/init_{code}.csv", index=False)
    return df

def load_fixtures_and_mk_datasets(league_id, csv_path):
  fix_path = f"../dat/football/fixtures_{league_id}.json"
  jf = load_json(fix_path)
  # print(len(jf["api"]["fixtures"]))
  _fixture_id,_day,_ref,_home_id,_home_team,_away_id,_away_team,_sc0,_sc1, _extra,_penalty=[],[],[],[],[],[],[],[],[],[],[]
  for ele in list(jf["api"]["fixtures"]):
    _fixture_id.append(ele["fixture_id"])
    _day.append(ele["event_date"])
    _ref.append(ele["referee"])
    _home_id.append(ele["homeTeam"]["team_id"])
    _home_team.append(ele["homeTeam"]["team_name"])
    _away_id.append(ele["awayTeam"]["team_id"])
    _away_team.append(ele["awayTeam"]["team_name"])
    _sc0.append(ele["score"]["halftime"])
    _sc1.append(ele["score"]["fulltime"])
    _extra.append(ele["score"]["extratime"])
    _penalty.append(ele["score"]["penalty"])
  
  df = pd.DataFrame()
  df["fixture_id"] = _fixture_id
  df["day"] = _day
  df["time"] = pd.to_datetime(df["day"])
  df = df.drop("day", axis=1)
  df["month"] = df["time"].apply(lambda x: x.month)

  df["referee"] = _ref
  df["home_id"] = _home_id
  df["home_team"] = _home_team
  df["away_id"] = _away_id
  df["away_team"] = _away_team
  df["score_half"] = _sc0
  df["score_full"] = _sc1
  df["score_half_home"] = df["score_half"].apply(lambda x: int(x.split("-")[0]))
  df["score_half_away"] = df["score_half"].apply(lambda x: int(x.split("-")[1]))
  df["score_full_home"] = df["score_full"].apply(lambda x: int(x.split("-")[0]))
  df["score_full_away"] = df["score_full"].apply(lambda x: int(x.split("-")[1]))
  df["extratime"] = _extra
  df["penalty"] = _penalty

  # print(df.head())
  df.to_csv(csv_path, index=False)
  print("make end.. game data stats...")
  return

def select_team_data(df_master, team_name, csv_path):
  if os.path.exists(csv_path):
    print(f"already select team stats... {team_name}")
    return
  else:
    oita = df_master.loc[(df_master["home_team"] == team_name) | (df_master["away_team"] == team_name),:]
    oita.to_csv(csv_path, index=False)
    print(f"Now and End to select team stats... {team_name}")
    return

if __name__ == "__main__":
  # df = load_league("JP")

  league_id = 283
  csv_master_path = f"../out/football/csv/master_{league_id}.csv"
  # make fixtures datas
  # load_fixtures_and_mk_datasets(league_id, csv_master_path)
  # sys.exit()
  master = pd.read_csv(csv_master_path)
  team_name = 'Oita Trinita'
  csv_path = f"../out/football/csv/team_fixture_oita.csv"
  select_team_data(master,team_name,csv_path)
  sys.exit()

  df = pd.read_csv(oita_csv)
  _fix_id = df["fixture_id"].values.tolist()
  for fix_id in _fix_id[:10]:
    print(fix_id)

  print(_fix_id[:15])
  sys.exit()

  sys.exit()