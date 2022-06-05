from nba_api.stats.endpoints import leaguedashplayerstats
from data_preparation.id_receiver import IDReceive as id
import json
import pandas as pd


def main():
    for year in range(0, 26):
        team_json = leaguedashplayerstats.LeagueDashPlayerStats(
            season=f'{1996 + year}-{str(1996 + year + 1)[2:]}')

        team_data = json.loads(team_json.get_json())
        relevant_data = team_data['resultSets'][0]
        headers = relevant_data['headers']
        rows = relevant_data['rowSet']

        total = pd.DataFrame(rows)
        total.columns = headers
        total['team_name'] = total['TEAM_ID'].apply(id.get_team_name)

        player_data = {team: {} for team in total['team_name'].unique()}
        for i in range(len(total)):
            player = total.iloc[i]
            player_data[player['team_name']].update(
                {player['PLAYER_NAME']: player.to_dict()})

        players_in_team = {team: list(
            (name, player_data[team][name]['PLAYER_ID'])
            for name in player_data[team].keys()) for team in player_data}

        with open(f'player_data/{1996 + year}-{str(1996 + year + 1)[2:]}.json',
                  'w') as f:
            json.dump(player_data, f)
        with open(f'player_data/{1996 + year}-{str(1996 + year + 1)[2:]}' +
                  '_players_in_team.json', 'w') as f:
            json.dump(players_in_team, f)


if __name__ == '__main__':
    main()
