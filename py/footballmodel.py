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

url = "https://api-football-v1.p.rapidapi.com/v2/predictions/157462"
url = "https://api-football-v1.p.rapidapi.com/v2/countries"
env = pd.read_csv("../env/football.env", header=None).set_index(0)
headers = {
  "x-rapidapi-host": env.loc["x-rapidapi-host"].values[0],
  "x-rapidapi-key": env.loc["x-rapidapi-key"].values[0]
}

# print(headers)

# sys.exit()

class GetFootballLeagueInfo:
  def __init__(self, code='JP', league_name='J. League Div.1'):
    self.code = code
    self.league_name = league_name
    self._season = []
    self._league_id = []
  
  def get_league(self,isReturn=False):
    url =f"https://api-football-v1.p.rapidapi.com/v2/leagues/country/{self.code}"
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    # print(data["api"]["leagues"])
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
  
  def get_year_result(self, year):
    if len(self._season) == 0:
      self.get_league(isReturn=False)
    idx = self._season.index(year)
    id0 = self._league_id[idx]
    url = f"https://api-football-v1.p.rapidapi.com/v2/teams/league/{id0}"
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    data = data["api"]["teams"]
    _df = [d for d in data]
    df = pd.DataFrame(_df)
    return df
    

def get_team_statics(season=2019, team=298, league=283):
  # https://api-football-beta.p.rapidapi.com/teams/statistics
  # url = f"https://api-football-v1.p.rapidapi.com/v2/teams/statistics?season={season}&team={team}&league={league}"
  url = f"https://api-football-v1.p.rapidapi.com/v2/statistics/{league}/{team}"
  print(url)
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
  for f in glob.glob(f'{OUTD}/*.png'): os.remove(f)
  # -----------
  # get som infomations.....-----------
  ft = GetFootballLeagueInfo(code='JP', league_name='J. League Div.1')
  name_team = 'Oita Trinita'
  team_name2 = re.sub(" ", "", name_team)
  _season, _league_id_team, _team_id = ft.get_result(name_team=name_team)
  # _s_oita, _lid_oita, _team_id = ft.get_result(name_team='Gamba Osaka')

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