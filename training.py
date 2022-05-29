import pandas as pd
import numpy as np
import json

win_data = pd.read_csv('C:/Users/jacky/OneDrive/UW/CSE/163/Final Project/past_win_pct/1996-97_winning_rate.csv')
win_pct = win_data['W_PCT'].to_numpy()
win_pct_team_name = win_data['TEAM_NAME'].to_numpy()
win_pct_team_id = win_data['TEAM_ID'].to_numpy()

with open('C:/Users/jacky/OneDrive/UW/CSE/163/Final Project/player_data/1996-97_players_in_team.json') as f:
    players_in_team = json.load(f)
    team_list = players_in_team.keys()

with open('C:/Users/jacky/OneDrive/UW/CSE/163/Final Project/player_data/1996-97.json') as f:
    players_data = json.load(f)

year_info = []
for team in team_list:
    player = []
    for player_info in players_data[team].values():
        data = list(player_info.values())[3:32]
        data[7] = data[7] / data[3]
        data.pop(1)
        data = np.array(data)
        player.append(data)
    player.sort(key=lambda x: x[6], reverse=True)
    team_info = np.vstack(tuple(player[:12]))
    print(team_info.shape)
    year_info.append(team_info)
total_data = np.vstack(tuple(year_info))