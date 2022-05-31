import pandas as pd
import numpy as np
import json
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import os


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
    total_data = pd.DataFrame(np.stack(tuple(total), axis=0))
    total_data.columns = [f'{lable}' for lable in range(90)]
    total_win_pct = pd.DataFrame(total_win_pct)

    train_data, test_data, train_win_pct, test_win_pct = train_test_split(
        total_data, total_win_pct, test_size=0.2)

    NUMERIC_COLUMNS = [f'{lable}' for lable in range(90)]
    feature_columns = [tf.feature_column.numeric_column(
        key, dtype=tf.float32) for key in NUMERIC_COLUMNS]
    
    linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns)

    train_input_fn = make_input_fn(train_data, train_win_pct)  # here we will call the input_function that was returned to us to get a dataset object we can feed to the model
    eval_input_fn = make_input_fn(test_data, test_win_pct, num_epochs=1, shuffle=False)
    linear_est.train(train_input_fn)
    result = linear_est.evaluate(eval_input_fn)
    print(result['accuracy'])


def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
    def input_function():  # inner function, this will be returned
        # create tf.data.Dataset object with data and its label
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
        if shuffle:
            ds = ds.shuffle(1000)  # randomize order of data
        # split dataset into batches of 32 and repeat process for number of epochs
        ds = ds.batch(batch_size).repeat(num_epochs)
        return ds  # return a batch of the dataset
    return input_function  # return a function object for use


if __name__ == "__main__":
    main()
