import pandas as pd
import numpy as np
import json
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import warnings
warnings.filterwarnings("ignore")


def main():
    total = []
    total_win_pct = []
    for year in range(0, 26):
        win_data = pd.read_csv(
            f'C:/Users/jacky/OneDrive/UW/CSE/163/Final Project/past_win_pct/{1996 + year}-{str(1996 + year + 1)[2:]}_winning_rate.csv')
        win_pct = win_data['W_PCT']
        win_pct.index = win_data['TEAM_ID']

        with open(f'C:/Users/jacky/OneDrive/UW/CSE/163/Final Project/player_data/{1996 + year}-{str(1996 + year + 1)[2:]}_players_in_team.json') as f:
            players_in_team = json.load(f)
            team_list = players_in_team.keys()

        players_num = 0
        teams = []
        for team in team_list:
            player = []
            id = 0
            with open(f'C:/Users/jacky/OneDrive/UW/CSE/163/Final Project/player_data/{1996 + year}-{str(1996 + year + 1)[2:]}.json') as f:
                players_data = json.load(f)
            for player_info in players_data[team].values():
                data = []
                data.extend((player_info['MIN_RANK'], player_info['FGM_RANK'],
                             player_info['FG_PCT_RANK'],
                             player_info['PTS_RANK'], player_info['REB_RANK'], player_info['AST_RANK'],
                             player_info['STL_RANK'], player_info['BLK_RANK'], player_info['TOV_RANK']))
                data = np.array(data, dtype=np.float32)
                player.append(data)
                id = player_info['TEAM_ID']
                players_num += 1
            player.sort(key=lambda x: x[0])
            team_info = np.vstack(tuple(player[:10])).reshape(-1, 1).squeeze()
            teams.append(team_info)
            total_win_pct.append((win_pct[id] * 1000).astype(np.int32) // 200)
        for i in range(len(team_list)):
            teams[i] = (players_num - teams[i]) / players_num
        total.extend(teams)

    NUMERIC_COLUMNS = []
    lables = [[f'MIN_RANK{i}' for i in range(10)],
              [f'FGM_RANK{i}' for i in range(10)],
              [f'FG_PCT_RANK{i}' for i in range(10)],
              [f'PTS_RANK{i}' for i in range(10)],
              [f'REB_RANK{i}' for i in range(10)],
              [f'AST_RANK{i}' for i in range(10)],
              [f'STL_RANK{i}' for i in range(10)],
              [f'BLK_RANK{i}' for i in range(10)],
              [f'TOV_RANK{i}' for i in range(10)]]
    for i in range(10):
        for j in range(9):
            NUMERIC_COLUMNS.append(lables[j][i])

    total_data = pd.DataFrame(np.stack(tuple(total), axis=0))
    total_data.columns = NUMERIC_COLUMNS
    total_win_pct = pd.DataFrame(total_win_pct)
    print(total_win_pct.shape)

    train_data, test_data, train_win_pct, test_win_pct = train_test_split(
        total_data, total_win_pct, test_size=0.2)
    
    def train_input_fn():
        return input_fn(train_data, NUMERIC_COLUMNS, train_win_pct, training = True)

    def eval_input_fn():
        return input_fn(test_data, NUMERIC_COLUMNS, test_win_pct, training = True)

    engineered_features = []

    for continuous_feature in NUMERIC_COLUMNS:
        engineered_features.append(
            tf.feature_column.numeric_column(continuous_feature))
    
    regressor = tf.estimator.DNNRegressor(
        feature_columns=engineered_features, hidden_units=[10, 10])

    wrap = regressor.train(input_fn=train_input_fn, steps=500)
    print('Evaluating ...')
    results = regressor.evaluate(input_fn=eval_input_fn, steps=1)
    for key in sorted(results):
        print("%s: %s" % (key, results[key]))


def input_fn(df, NUMERIC_COLUMNS, win_pct, training = True):
    # Creates a dictionary mapping from each continuous feature column name (k) to
    # the values of that column stored in a constant Tensor.
    continuous_cols = {k: tf.constant(df[k].values)
                       for k in NUMERIC_COLUMNS}

    # Merges the two dictionaries into one.
    feature_cols = dict(list(continuous_cols.items()))

    if training:
        # Converts the label column into a constant Tensor.
        label = tf.constant(win_pct.values)

        # Returns the feature columns and the label.
        return feature_cols, label
    
    # Returns the feature columns    
    return feature_cols


if __name__ == "__main__":
    main()
