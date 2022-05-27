from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

teams = json.loads(requests.get(
    'https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
players = json.loads(requests.get(
    'https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)


def get_team_id(queried_team):
    for team in teams:
        if team['teamName'] == queried_team:
            return team['teamId']
    return -1


def get_player_id(first, last):
    for player in players:
        if player['firstName'] == first and player['lastName'] == last:
            return player['playerId']
    return -1


shot_json = shotchartdetail.ShotChartDetail(
    team_id=get_team_id('Golden State Warriors'),
    player_id=get_player_id('Klay', 'Thompson'),
    context_measure_simple='FGA',
    season_nullable='2015-16',
    season_type_all_star='Regular Season')


shot_data = json.loads(shot_json.get_json())

# Get the relevant data from our dictionary
relevant_data = shot_data['resultSets'][0]

headers = relevant_data['headers']
rows = relevant_data['rowSet']

curry_data = pd.DataFrame(rows)
curry_data.columns = headers


def create_court(ax, color):
    # Short corner 3PT lines
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
    ax.hexbin(curry_data['LOC_X'], curry_data['LOC_Y'] + 60, gridsize=(50,
              50), extent=(-300, 300, 0, 940), bins='log', cmap='Blues')


def main():
    mpl.rcParams['axes.linewidth'] = 2
    with open('output.json', 'w') as outfile:
        json.dump(relevant_data, outfile)
    fig = plt.figure(figsize=(4, 3.76))
    ax = fig.add_axes([0, 0, 1, 1])
    ax = create_court(ax, 'black')
    fig.savefig('thompson_shot_chart.png', dpi=300)
    plt.show()


if __name__ == '__main__':
    main()