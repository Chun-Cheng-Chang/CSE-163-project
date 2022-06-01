import pandas as pd
import numpy as np
import json
from tensorflow import keras
from sklearn.model_selection import train_test_split


def main():
    total = []
    total_win_pct = []
    for year in range(0, 26):
        win_data = pd.read_csv(
            f'past_win_pct/{1996 + year}-{str(1996 + year + 1)[2:]}' +
            '_winning_rate.csv')
        win_pct = win_data['W_PCT']
        win_pct.index = win_data['TEAM_ID']

        with open(f'player_data/{1996 + year}-{str(1996 + year + 1)[2:]}' +
                  '_players_in_team.json') as f:
            players_in_team = json.load(f)
            team_list = players_in_team.keys()

        players_num = 0
        teams = []
        for team in team_list:
            player = []
            id = 0
            with open(f'player_data/{1996 + year}-{str(1996 + year + 1)[2:]}' +
                      '.json') as f:
                players_data = json.load(f)
            for players in players_data[team].values():
                data = []
                data.extend((players['MIN_RANK'], players['FGM_RANK'],
                             players['FG_PCT_RANK'], players['FG3M_RANK'],
                             players['FG3_PCT_RANK'], players['PTS_RANK'],
                             players['REB_RANK'], players['AST_RANK'],
                             players['STL_RANK'], players['BLK_RANK'],
                             players['TOV_RANK']))
                data = np.array(data, dtype=np.float32)
                player.append(data)
                id = players['TEAM_ID']
                players_num += 1
            player.sort(key=lambda x: x[0])
            team_info = np.vstack(tuple(player[:12]))
            teams.append(team_info)
            total_win_pct.append((win_pct[id] * 1000).astype(np.int32) // 200)
        for i in range(len(team_list)):
            teams[i] = (players_num - teams[i]) / players_num
        total.extend(teams)
    total_data = np.stack(tuple(total), axis=0)
    print(total_data.shape)
    total_win_pct = np.array(total_win_pct)
    print(total_win_pct.shape)

    train_data, test_data, train_win_pct, test_win_pct = train_test_split(
        total_data, total_win_pct, test_size=0.2)

    best_model = None
    best_acc = 0
    for i in range(10):
        for j in range(45, 90):
            for k in range(45, 70):
                model = keras.Sequential([
                    keras.layers.Flatten(input_shape=(
                        12, 11)),  # input layer (1)
                    # hidden layer (2)
                    keras.layers.Dense(j, activation='relu'),
                    # hidden layer (2)
                    keras.layers.Dense(k, activation='relu'),
                    # hidden layer (2)
                    keras.layers.Dense(k, activation='relu'),
                    # output layer (3)
                    keras.layers.Dense(5, activation='softmax')
                ])
                model.compile(optimizer='adam',
                              loss='mean_squared_error',
                              metrics=['accuracy'])
                model.fit(train_data, train_win_pct, epochs=4)
                test_loss, test_acc = model.evaluate(
                    test_data,  test_win_pct, verbose=1)
                if test_acc > best_acc:
                    best_acc = test_acc
                    best_model = model

    print('Test accuracy:', best_acc)
    best_model.save(f'model/overall_modelV2_acc={best_acc:.2f}.h5')


if __name__ == '__main__':
    main()
