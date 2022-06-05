import pandas as pd

COLUMNS = ['TEAM_ID', 'Player_Name', 'Season', 'age', 'team_w_pct', 'GP',
           'w_pct', 'min/game', 'PTS/game', 'FG_pct', 'FG3_pct', 'REB/game',
           'AST/game', 'STL/game', 'BLK/game', 'TOV/game', 'Plus_Minus',
           'salary']


def main():
    raw = pd.read_csv('Q3/total_player_data.csv')
    target_data_columns = COLUMNS[3:]
    target_data_columns.pop(1)
    target_data_columns.pop(2)
    df = pd.DataFrame()
    for col in target_data_columns:
        df[(col + "_std")] = raw.groupby(['TEAM_ID', 'Season'])[col].std()
        df[(col + "_mean")] = raw.groupby(['TEAM_ID', 'Season'])[col].mean()
    df['win_pct'] = raw.groupby(['TEAM_ID', 'Season'])['team_w_pct'].mean()
    df.to_csv('Q3/winning_rate_training_data.csv', index=False)


if __name__ == '__main__':
    main()
