"""
This file is used to plot the shot chart for a player.
"""

from nba_api.stats.endpoints import shotchartdetail
import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from id_receiver import IDReceive as id


def get_shot_data(team_id, player_id, season, season_type='Regular Season',
                  plot_type='FGM'):
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
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.plot([-30, 30], [40, 40], linewidth=4, color=color)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    cmap = {'FGA': 'Greens', 'FGM': 'Blues'}
    ax.hexbin(player_shot_data['LOC_X'], player_shot_data['LOC_Y'] + 60,
              gridsize=(50, 50), extent=(-300, 300, 0, 940),
              cmap=cmap[plot_type], bins='log')
    ax.add_artist(mpl.patches.Circle(
        (0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    ax.add_artist(mpl.patches.Circle(
        (0, 60), 15, facecolor='none', edgecolor=color, lw=3))
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0,
                  theta2=180, facecolor='none', edgecolor=color, lw=2))


def save(player_data, plot_type='FGM', save_path='Q1/player_shots.png'):
    """
    This function is used to save the shot chart.
    """
    mpl.rcParams['axes.linewidth'] = 2
    fig = plt.figure(figsize=(4, 3.76))
    ax = fig.add_axes([0, 0, 1, 1])
    ax = create_court(ax, 'black', player_data, plot_type)
    fig.savefig(save_path, dpi=300)
    plt.show()
    plt.close('all')


def main():
    first = input('Enter first name: ')
    last = input('Enter last name: ')
    team = input('Enter team name: ')
    season = input('Enter season: ')
    player_id = id.get_player_id(first, last)
    shot_data = get_shot_data(id.get_team_id(team), player_id,
                              season, 'Regular Season', 'FGM')
    save(shot_data)


if __name__ == '__main__':
    main()
