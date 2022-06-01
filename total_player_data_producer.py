import pandas as pd
import json


def main():
    catagory = ['Player_Name', 'Season', 'age', 'team_w_pct', 'GP', 'w_pct',
                'min/game', 'PTS/game', 'FG_pct', 'FG3_pct', 'REB/game',
                'AST/game', 'STL/game', 'BLK/game', 'TOV/game', 'Plus_Minus',
                'salary']
    player_info = []
    for year in range(0, 26):
        win_data = pd.read_csv(
            f'past_win_pct/{1996 + year}-{str(1996 + year + 1)[2:]}' +
            '_winning_rate.csv')
        win_pct = win_data['W_PCT']
        win_pct.index = win_data['TEAM_ID']

        df = pd.read_csv(
            f'salary/{1996 + year}-{1997 + year}_salary.csv')
        salary = df['SALARY']
        salary.index = df['PLAYER']
        salary_data = salary.to_dict()

        with open(f'player_data/{1996 + year}-{str(1996 + year + 1)[2:]}' +
                  '.json') as f:
            players_data = json.load(f)
        for team in players_data.values():
            for player in team.values():
                if player['PLAYER_NAME'] in salary_data.keys():

                    game_played = player['GP']
                    information = [player['PLAYER_NAME'],
                                   f'{1996 + year}-{str(1996 + year + 1)[2:]}',
                                   player['AGE'], win_pct[player['TEAM_ID']],
                                   game_played, player['W_PCT'],
                                   player['MIN'] / game_played,
                                   player['PTS'] / game_played,
                                   player['FG_PCT'], player['FG3_PCT'],
                                   player['REB'] / game_played,
                                   player['AST'] / game_played,
                                   player['STL'] / game_played,
                                   player['BLK'] / game_played,
                                   player['TOV'] / game_played,
                                   player['PLUS_MINUS'],
                                   salary_data[player['PLAYER_NAME']]]
                    player_info.append(information)

    total_data = pd.DataFrame(player_info)
    total_data.columns = catagory
    total_data.to_csv('total_player_data.csv')


if __name__ == "__main__":
    main()
