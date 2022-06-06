"""
This file is used to check the accuracy of the model by using the actual
winning rate to compare with the prediction.
"""

import pandas as pd
import numpy as np
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


"""
features catagory: std => standard deviation, mean => mean
age_std, age_mean, GP_std, GP_mean, min/game_std, min/game_mean, PTS/game_std,
PTS/game_mean, FG_pct_std, FG_pct_mean, FG3_pct_std, FG3_pct_mean,
REB/game_std, REB/game_mean, AST/game_std, AST/game_mean, STL/game_std,
STL/game_mean, BLK/game_std, BLK/game_mean, TOV/game_std, TOV/game_mean,
Plus_Minus_std, Plus_Minus_mean, salary_std, salary_mean

lables:
    0: 0 <= winning rate < 0.2,
    1: 0.2 <= winning rate < 0.4,
    2: 0.4 <= winning rate < 0.6,
    3: 0.6 <= winning rate < 0.8,
    4: 0.8 <= winning rate < 1
"""


def main():
    raw = pd.read_csv('Q3/winning_rate_training_data.csv')
    features = raw.drop(['win_pct'], axis=1).to_numpy()

    def winning_rate_range(win_pct):
        win_pct_range = int(win_pct * 1000) // 200
        return win_pct_range

    lables = raw['win_pct'].apply(winning_rate_range).to_list()

    model = tf.keras.models.load_model(
        'Q3/best_winning_rate_model_acc=0.52.h5')
    prediction = model.predict(features)
    prediction = np.split(prediction, 772)

    correct = 0
    incorrect = 0
    differences = {}
    for result, ans in zip(prediction, lables):
        predict = np.argmax(result)
        if predict == ans:
            correct += 1
        else:
            incorrect += 1
        difference = abs(predict - ans)
        if difference not in differences:
            differences[difference] = 0
        differences[difference] += 1
    print(f'\nCorrect: {correct}')
    print(f'Incorrect: {incorrect}')
    print(f'Accuracy: {correct / (correct + incorrect):.2f}')
    print(f'Differences: {sorted(differences.items(), key=lambda x: x[0])}')


if __name__ == '__main__':
    main()
