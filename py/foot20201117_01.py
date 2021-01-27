
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
from footballmodel import GetFootballLeagueInfo
from footballmodel import get_team_statics #(season=2019, team=298, league=283):
from footballmodel import plot_pie #(ax, df, col)


def get_year_teams(ft,year):
  df = ft.get_year_result(year)
  if os.path.exists(f"../tbl/{year}_j1.csv"):
    print("already save team data...")
  else:
    df.to_csv(f"../tbl/{year}_j1.csv", index=False)
  print(df["name"].values.tolist())
  return

def cut_season(_season, _league_id_team, _team_id, use_years=3):
  tmp = pd.DataFrame()
  tmp["season"] = _season
  tmp["league_id"] = _league_id_team
  tmp["team_id"] = _team_id
  tmp = tmp.sort_values("season", ascending=False)

  _season = tmp["season"].values.tolist()[:use_years]
  _league_id_team= tmp["league_id"].values.tolist()[:use_years]
  _team_id = tmp["team_id"].values.tolist()[:use_years]
  return _season,_league_id_team,_team_id


def load_json(json_path):
  with open(json_path, "r") as json_file:
    json_data = json.load(json_file)
  return json_data

if __name__ == "__main__":
  #init remover--------------------
  OUTD='../out/png1'
  # for f in glob.glob(f'{OUTD}/*.png'): os.remove(f)
  # -----------
  # get som infomations.....-----------
  ft = GetFootballLeagueInfo(code='JP', league_name='J. League Div.1')
  # _season, _league_id = ft.get_league(isReturn=True)
  # year = 2020
  # get_year_teams(ft, year)
  # sys.exit()
  _name_team = ['Oita Trinita','Kawasaki Frontale','Vissel Kobe','Sagan Tosu']
  # _s_oita, _lid_oita, _team_id = ft.get_result(name_team='Gamba Osaka')

  for name_team in _name_team:
    name_team='Sagan Tosu'
    team_name2 = re.sub(" ", "", name_team)
    _season, _league_id_team, _team_id = ft.get_result(name_team=name_team)
    _season, _league_id_team, _team_id = cut_season(_season, _league_id_team, _team_id, use_years=3)
    # print(_season, _league_id_team, _team_id)
    # sys.exit()
    #------------------------------
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
    print(f"end {team_name2}...")
    #------------------------------
    # sys.exit()
    
  # conn.request("GET", "/teams/statistics?season=2019&team=298&league=283"
  # sys.exit()