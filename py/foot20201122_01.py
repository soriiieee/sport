
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

def get_fixtures_id(path):
  df = pd.read_csv(path)
  df["time"] = df["time"].apply(lambda x: x[:10])
  # print(df.head())
  _fix_id = list(df["fixture_id"].values)
  _time = list(df["time"].values)
  _referee = list(df["referee"].values)
  _home= list(df["home_team"].values)
  _away = list(df["away_team"].values)
  _score_half = list(df["score_half"].values)
  _score_full = list(df["score_full"].values)

  return _time, _fix_id,_referee,_home,_away,_score_half,_score_full

def conv_team_fixture(fix_id,cate,sc_h,sc_f):
  fix_path = f"../dat/football/fix_{cate}/{fix_id}.json"
  data = load_json(fix_path)
  # print(data["api"]["statistics"])
  df = pd.DataFrame(data["api"]["statistics"]).T
  # df.append(pd.Series())
  s0 = pd.Series(sc_h.split("-"), name="half_score", index=["home","away"])
  s1 = pd.Series(sc_f.split("-"), name="full_score", index=["home","away"])
  # names = pd.Series([,], name="full_score", index=["home","away"])
  df = df.append(s0)
  df = df.append(s1)
  # df = df.reset_index()
  # print(df.head(15))
  # sys.exit()
  return df

def conv_player_fixture(fix_id,cate,sc_h,sc_f):
  fix_path = f"../dat/football/fix_{cate}/{fix_id}.json"
  data = load_json(fix_path)
  # print(data["api"]["players"])
  return data["api"]["players"]

def add_info_team_fixtures(df, _col, _param):
  # name_home = _param[3]
  # name_away = _param[4]
  # names = pd.Series([name_home, name_away], name="team_name", index=["home", "away"])
  for col, ele in zip(_col, _param):
    df[col] = ele
  # print(df.head(10))
  return df

def mk_team_fixtues_csv_from_json(team_path, csv_out_path):
  _df = []
  _time, _fix_id, _referee, _home, _away, _score_half, _score_full = get_fixtures_id(team_path)
  for time, fix_id, referee, home,away,sc_h,sc_f in zip(_time, _fix_id, _referee,_home,_away,_score_half,_score_full):
    _param = [ time, fix_id, referee, home, away]
    _col = [ "time","fix_id", "referee", "home_team", "away_team"]
    # csv_path = f"../out/football/fix_{cate}/{fix_id}.csv"
    try:
      df = conv_team_fixture(fix_id, cate, sc_h, sc_f)
      # df = add_info_team_fixtures(df, _col, _param)
      if int(sc_f.split("-")[0]) > int(sc_f.split("-")[1]):
        points,results = [3,0],["win","lose"]
      elif int(sc_f.split("-")[0]) == int(sc_f.split("-")[1]):
        points,results = [1,1],["draw","draw"]
      else:
        points,results= [0,3],["lose","win"]
      _p = pd.Series(points, name="result_point", index=["home", "away"])
      _r = pd.Series(results, name="result", index=["home", "away"])
      df = df.append(_p)
      df = df.append(_r)
      df = add_info_team_fixtures(df, _col, _param)
      # homdf.loc[df["index"] == "full_score",["home","away"]].values[0])
      _df.append(df)
    except:
      print(f"error json2 csv.. {fix_id}")
    print(f"end {fix_id}-{time}...")
  
  df = pd.concat(_df, axis=0)
  df = df.reset_index()
  df.loc[df["index"] == "Ball Possession", "home"] = df.loc[df["index"] == "Ball Possession", "home"].apply(lambda x: int(x.split("%")[0]))
  df.loc[df["index"] == "Ball Possession","away"] = df.loc[df["index"] == "Ball Possession","away"].apply(lambda x: int(x.split("%")[0]))
  # sys.exit()
  # df = df.reset_index()
  df.to_csv(csv_out_path, index=False)
  return

def mk_player_fixtues_csv_from_json(team_path, csv_out_path):
  _time, _fix_id, _referee, _home, _away, _score_half, _score_full = get_fixtures_id(team_path)
  
  _df_all = []
  for time, fix_id, referee, home,away,sc_h,sc_f in zip(_time, _fix_id, _referee,_home,_away,_score_half,_score_full):
    _param = [ time, fix_id, referee, home, away]
    _col = ["time", "fix_id", "referee", "home_team", "away_team"]
    data = conv_player_fixture(fix_id, cate, sc_h, sc_f)
    # df_all = pd.DataFrame()
    df_all =[]
    for i, e in enumerate(data):
      dicts = {}
      for key in list(e.keys()):
        if type(e[key]) != dict:
          dicts[key] = e[key]
        else:
          for key2, value in e[key].items():
            # print(key2, value)
            # sys.exit()
            dicts[f"{key}_{key2}"] = value
          # sys.exit()
      df = pd.DataFrame()
      df["cate"] = dicts.keys()
      df[i] = dicts.values()
      df = df.set_index("cate")
      df_all.append(df)
      # print(df_all.head())
      print(f"[END]: {time} - {dicts['player_name']}")
    
    df = pd.concat(df_all, axis=1)
    df = df.T
    df["time"] = time
    _df_all.append(df)
  
  df = pd.concat(_df_all, axis=0)
  df.to_csv(csv_out_path, index=False)
  return

if __name__ == "__main__":
  # df = load_league("JP")
  # fixtures id get 
  team_path = f"../out/football/csv/team_fixture_oita.csv"
  
  isRun=0
  cate = "player"
  team_name = "oita"  #if you make ,get team_fixtures_datasets(json)...
  if isRun:
    if cate == "team":
      print(f"[NOW]: making [{team_name}] team-datasets")
      csv_out_path = f"../out/football/csv/{team_name}_{cate}_stats.csv"
      mk_team_fixtues_csv_from_json(team_path, csv_out_path)
    if cate == "player":
      print(f"[NOW]: making [{team_name}] player-datasets")
      csv_out_path = f"../out/football/csv/{team_name}_{cate}_stats.csv"
      mk_player_fixtues_csv_from_json(team_path, csv_out_path)
  else:
    print("No exec..",isRun)

  sys.exit()