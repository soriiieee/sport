# https://api.rakuten.net/api-sports/api/api-football?endpoint=apiendpoint_33b2c650-e8fb-4ac6-aa3c-715d2bb5032f
# reference

import numpy as np
import sys, os, re, glob
import re
# sys.path.append('/Users/soriiieee/.local/lib/python3.7/site-packages')
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

import requests
import json
import time

try:
  headers = {
    "x-rapidapi-host": open("../env2/api_host.env").read(),
    "x-rapidapi-key": open("../env2/api_football_key.env").read()
  }
except:
  print("please get your [Rakuten YOUR_API_KEY...] ")
  print("1: you click and get your api key -> https://api.rakuten.net/api-sports/api/api-football")
  print("2-1: you make ../env2/api_host.env and write API_HOST_URL )
  print("2-2: you make ../env2/api_football_key.env and write YOUR_API_KEY )

# sys.exit()

def load_json(json_path):
  with open(json_path, "r") as json_file:
    json_data = json.load(json_file)
  return json_data

class GetFootballLeagueInfo:
  def __init__(self, code='JP', league_name='J. League Div.1'):
    self.code = code
    self.league_name = league_name
    self._season = []
    self._league_id = []
    if os.path.exists(f"../dat/football/init_json_{self.code}.json"):
      print("[Already] init json ... ")
    else:
      url =f"https://api-football-v1.p.rapidapi.com/v2/leagues/country/{self.code}"
      response = requests.request("GET", url, headers=headers)
      data = response.json()
      with open(f"../dat/football/init_json_{self.code}.json", "w") as f:
        json.dump(data,f)
      print("[Now] init json ... ")
  
  def get_fixtures(self,league_id,fixtures_path):
    # querystring = {"timezone":"Europe%2FLondon"}
    if os.path.exists(fixtures_path):
      print("[Already] get_fixtures json ... ")
    else:
      url = f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{league_id}"
      response = requests.request("GET", url, headers=headers)
      data = response.json()
      with open(fixtures_path, "w") as f:
        json.dump(data,f)
      print("[Now] get_fixtures json ... ")

  
  def get_league(self,isReturn=False):
    url =f"https://api-football-v1.p.rapidapi.com/v2/leagues/country/{self.code}"
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    # print(data["api"]["leagues"])
    # sys.exit()
    _season=[]
    _league_id=[]

    for r in data["api"]["leagues"]:
      if r["name"] ==self.league_name:
        _season.append(r["season"])
        _league_id.append(r["league_id"])
    
    self._season = _season
    self._league_id = _league_id

    if isReturn:
      return _season, _league_id
    else:
      return
  
  def get_result(self,name_team= 'Oita Trinita'):
    _s_oita, _lid_oita, _team_id = [], [], []
    if len(self._season) ==0:
      self.get_league(isReturn=False)
    
    for s,id0 in zip(self._season,self._league_id):
      # print(s,id)
      url = f"https://api-football-v1.p.rapidapi.com/v2/teams/league/{id0}"
      response = requests.request("GET", url, headers=headers)
      data = response.json()
      for r in list(data["api"]["teams"]):
        if r["name"] == name_team:
          _s_oita.append(s)
          _lid_oita.append(id0)
          _team_id.append(r["team_id"])
    return _s_oita, _lid_oita, _team_id
  
  def get_year_result(self, year, csv_path):
    if os.path.exists(csv_path):
      return
    # if len(list(self._season)) == 0:
    self.get_league(isReturn=False)
    # print(type(self._season))
    # sys.exit()
    # print(self._season)
    # sys.exit()
    idx = self._season.index(year)
    id0 = self._league_id[idx]
    url = f"https://api-football-v1.p.rapidapi.com/v2/teams/league/{id0}"
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    data = data["api"]["teams"]
    _df = [d for d in data]
    df = pd.DataFrame(_df)
    df.to_csv(csv_path,index=False)
    return 
  
  def make_team_stats_csv_data(self, name_team, csv_path):
    if os.path.exists(csv_path):
      return 
    _season, _league_id_team, _team_id = self.get_result(name_team=name_team)
    df_team = pd.DataFrame()
    df_team["season"] = _season
    df_team["league_id"] = _league_id_team
    df_team["team_id"] = _team_id
    df_team.to_csv(csv_path,index=False)
    return
  
  def get_team_fixtures(self, fix_id, out_path):
    if os.path.exists(out_path):
      data = load_json(out_path)
      if "api" in data.keys():
        print(f"[Already] get_team_fixtures {fix_id}  ... ")
      else:
        os.remove(out_path)
        print(f"[Remove] fixtures(team) - No datas ... {fix_id}  ... ")
    else:
      url = f"https://api-football-v1.p.rapidapi.com/v2/statistics/fixture/{fix_id}/"
      response = requests.request("GET", url, headers=headers)
      data = response.json()
      with open(out_path, "w") as f:
        json.dump(data,f)
      print(f"[Now] get_team_fixtures {fix_id} ... ")
    return
  
  def get_player_fixtures(self, fix_id, out_path):
    if os.path.exists(out_path):
      data = load_json(out_path)
      if "api" in data.keys():
        print(f"[Already] get_player_fixtures {fix_id} ... ")
      else:
        os.remove(out_path)
        print(f"[Remove] fixtures(player)- No datas ... {fix_id}  ... ")
    else:
      url = f"https://api-football-v1.p.rapidapi.com/v2/players/fixture/{fix_id}"
      response = requests.request("GET", url, headers=headers)
      data = response.json()
      with open(out_path, "w") as f:
        json.dump(data,f)
      print(f"[Now] get_player_fixtures {fix_id} ... ")
    return
    

def get_team_statics(season=2019, team=298, league=283):
  # https://api-football-beta.p.rapidapi.com/teams/statistics
  # url = f"https://api-football-v1.p.rapidapi.com/v2/teams/statistics?season={season}&team={team}&league={league}"
  url = f"https://api-football-v1.p.rapidapi.com/v2/statistics/{league}/{team}"
  # print(url)
  # url = f"https://api-football-beta.p.rapidapi.com/teams/statistics?season={season}&team={team}&league={league}" 
  response = requests.request("GET", url, headers=headers)
  data = response.json()
  return data


def plot_pie(ax, df, col):
  def func(x, _val):
    percent = int(x / 100.*np.sum(_val))
    return "{:.1f}%\n({:d} game)".format(x, percent)
  ax.pie(df[col] * 100 / df[col].sum(), labels=df.index, autopct=lambda x: func(x, df[col].values),startangle=90)
  ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
  return ax
  

if __name__ == "__main__":
  #init remover--------------------
  OUTD='../out/png1'
  # for f in glob.glob(f'{OUTD}/*.png'): os.remove(f)

  #----------------------------------------------------
  # initial get infomation football Instance...-----------
  code = "JP"
  league_name='J. League Div.1'
  ft = GetFootballLeagueInfo(code=code, league_name=league_name)
  # sys.exit()

  #----------------------------------------------------
  # get _fixtures json ....
  """
  README.md...
  <in>
  :league_id = 283 is means -> {year : 2019 ,  league: j1 }
  =these code is get from init_JP.csv .if you open csv file, you get some local leagues infomation
  which is include competitions like Ruban Cup and Emperior New year tournaments...
  :fixtures_path =  you get json file which is return api datas temporaly file 

  these code is get from init_JP.csv .if you open csv file, you get some local leagues infomation
  which is include competitions like Ruban Cup and Emperior New year tournaments...
  """
  league_id = 283
  fixtures_path =f"../dat/football/fixtures_{league_id}.json"
  ft.get_fixtures(league_id,fixtures_path)
  # team_stats_path = f"../tbl/football/{year}_{code}.csv"
  # ft.get_year_result(year, team_stats_path)
  # sys.exit()
  #----------------------------------------------------

  team_fix_path= "../out/football/csv/team_fixture_oita.csv"
  df = pd.read_csv(team_fix_path)
  _fix_id = list(df["fixture_id"].values)

  for fix_id in _fix_id:
    out_fix_team_json_path = f"../dat/football/fix_team/{fix_id}.json"
    out_fix_player_json_path = f"../dat/football/fix_player/{fix_id}.json"

    ft.get_team_fixtures(fix_id, out_fix_team_json_path)
    time.sleep(2)
    ft.get_player_fixtures(fix_id, out_fix_player_json_path)
    # sys.exit()
  sys.exit()

  _fix_id = [112697, 112709, 112712, 112726, 112734, 112740, 112753, 112763, \
    112764, 112781, 112790, 112798, 112808, 112812, 112826]
  print(_fix_id)
  sys.exit()
  #----------------------------------------------------
  # year stats master making....
  #
  # year = 2016
  # team_stats_path = f"../tbl/football/{year}_{code}.csv"
  # ft.get_year_result(year, team_stats_path)
  # sys.exit()
  #----------------------------------------------------

  #----------------------------------------------------
  # team stats master making....
  #
  name_team = 'Oita Trinita'
  team_name2 = re.sub(" ", "", name_team)
  team_stats_csv_path = f"../out/football/csv/{team_name2}.csv"
  ft.make_team_stats_csv_data(name_team, team_stats_csv_path)
  #----------------------------------------------------
  sys.exit()


  f, ax = plt.subplots(len(_season), 2, figsize=(5*len(_season), 5*2))
  _i = np.arange(len(_season))
  for i,season, league_id_team, team_id in zip(_i,_season, _league_id_team, _team_id):
    data = get_team_statics(season=season, team=team_id, league=league_id_team)
    df = pd.DataFrame(data["api"]["statistics"]["matchs"]).T.drop(["total"], axis=1).iloc[1:,:]
    for j, place in enumerate(["home", "away"]):
      ax[i, j] = plot_pie(ax[i, j], df, col=place)
      ax[i, j].set_title(f"{team_name2}({season})\n{place} stats..",pad=-5)
      
  f.tight_layout()
  # plt.subplots_adjust(wspace=0., hspace=0.0)
  f.savefig(f"../out/png1/stats_{team_name2}.png", bbox_inches="tight")
  sys.exit()
    
  # conn.request("GET", "/teams/statistics?season=2019&team=298&league=283"
  # sys.exit()