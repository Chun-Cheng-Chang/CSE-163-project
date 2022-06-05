import pandas as pd
import numpy as np
import tensorflow as tf


"""
features catagory: std => standard deviation, mean => mean
age_std, age_mean, GP_std, GP_mean, min/game_std, min/game_mean, PTS/game_std,
PTS/game_mean, FG_pct_std, FG_pct_mean, FG3_pct_std, FG3_pct_mean,
REB/game_std, REB/game_mean, AST/game_std, AST/game_mean, STL/game_std,
STL/game_mean, BLK/game_std, BLK/game_mean, TOV/game_std, TOV/game_mean,
Plus_Minus_std, Plus_Minus_mean, salary_std, salary_mean

lables:
    0: 0 <= winning rate < 200,
    1: 200 <= winning rate < 400,
    2: 400 <= winning rate < 600,
    3: 600 <= winning rate < 800,
    4: 800 <= winning rate < 1000
"""


def main():
    raw = pd.read_csv('winning_rate_training_data.csv')
    features = raw.drop(['win_pct'], axis=1).to_numpy()

    def winning_rate_range(win_pct):
        win_pct_range = int(win_pct * 1000) // 200
        return win_pct_range

    lables = raw['win_pct'].apply(winning_rate_range).to_list()

    model = tf.keras.models.load_model('best_winning_rate_model_acc=0.54.h5')
    prediction = model.predict(features)
    prediction = np.split(prediction, 772)

    correct = 0
    incorrect = 0
    for result, ans in zip(prediction, lables):
        predict = np.argmax(result)
        if predict == ans:
            correct += 1
        else:
            incorrect += 1
    print(f'\nCorrect: {correct}')
    print(f'Incorrect: {incorrect}')
    print(f'Accuracy: {correct / (correct + incorrect):.2f}')


if __name__ == '__main__':
    main()
