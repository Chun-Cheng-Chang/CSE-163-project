"""
This file is used to create the shot chart for each player in each team in each
year.
Do not try to run this file; it's slow and will take a long time to run.
"""

import time
from nba_api.stats.endpoints import shotchartdetail
import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from id_receiver import IDReceive as id
import os


def get_shot_data(team_id, player_id, season, season_type, plot_type):
    """
    This function is used to get the shot data for players
    """
    shot_json = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=player_id,
        context_measure_simple=plot_type,
        season_nullable=season,
        season_type_all_star=season_type)
    shot_data = json.loads(shot_json.get_json())
    relevant_data = shot_data['resultSets'][0]
    headers = relevant_data['headers']
    rows = relevant_data['rowSet']
    player_shot_data = pd.DataFrame(rows, columns=headers)
    return player_shot_data


def create_court(ax, color, player_shot_data, plot_type):
    """
    This function is used to create the court for the shot chart.
    """
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0,
                  theta2=180, facecolor='none', edgecolor=color, lw=2))
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle(
        (0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    ax.add_artist(mpl.patches.Circle(
        (0, 60), 15, facecolor='none', edgecolor=color, lw=2))
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    cmap = {'FGA': 'Greens', 'FGM': 'Blues'}
    ax.hexbin(player_shot_data['LOC_X'], player_shot_data['LOC_Y'] + 60,
              gridsize=(50, 50), extent=(-300, 300, 0, 940), bins='log',
              cmap=cmap[plot_type])


def save(player_data, plot_type, save_path):
    """
    This function is used to save the shot chart.
    """
    mpl.rcParams['axes.linewidth'] = 2
    fig = plt.figure(figsize=(4, 3.76))
    ax = fig.add_axes([0, 0, 1, 1])
    ax = create_court(ax, 'black', player_data, plot_type)
    fig.savefig(save_path, dpi=300)
    plt.close('all')


def main():
    for year in range(0, 26):
        os.mkdir(f'Q1/shot_chart/{1996 + year}-{str(1996 + year + 1)[2:]}')
        os.mkdir(f'Q1/shot_chart/{1996 + year}-{str(1996 + year + 1)[2:]}/FGM')
        with open(f'data_preparation/player_data/{1996 + year}-' +
                  f'{str(1996 + year + 1)[2:]}' +
                  '_players_in_team.json') as json_file:
            player_data_in_year = json.load(json_file)
        for team in player_data_in_year.keys():
            os.mkdir(
                f'Q1/shot_chart/{1996 + year}-{str(1997 + year)[2:]}' +
                f'/FGM/{team}')
            for player, player_id in player_data_in_year[team]:
                shot_data = get_shot_data(id.get_team_id(team), player_id,
                                          f'{1996 + year}-' +
                                          f'{str(1996 + year + 1)[2:]}',
                                          'Regular Season', 'FGM')
                time.sleep(1.500)
                save(shot_data, 'FGM',
                     f'Q1/shot_chart/{1996 + year}-{str(1996 + year + 1)[2:]}'
                     + f'/FGM/{team}/{player}.png')


if __name__ == '__main__':
    main()
