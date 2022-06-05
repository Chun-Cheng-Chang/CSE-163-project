import pandas as pd
import numpy as np
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


"""
features catagory: std => standard deviation, mean => mean
Season, age, team_w_pct, GP, w_pct, min/game, PTS/game, FG_pct, FG3_pct,
REB/game, AST/game, STL/game, BLK/game, TOV/game, Plus_Minus

lables:
    0: 0 <= salary <= 1500000,
    1: 1500000 < salary <= 2500000,
    2: 2500000 < salary <= 6000000,
    3: 6000000 < salary <= 20000000,
    4: 20000000 < salary <= 30000000,
    5: 30000000 < salary
"""


def main():
    used_col = ['Season', 'age', 'team_w_pct', 'GP', 'w_pct', 'min/game',
                'PTS/game', 'FG_pct', 'FG3_pct', 'REB/game', 'AST/game',
                'STL/game', 'BLK/game', 'TOV/game', 'Plus_Minus']
    raw = pd.read_csv('Q2/total_player_data.csv')

    def salary_level(salary):
        if salary > 30000000:
            return 5
        elif salary > 20000000:
            return 4
        elif salary > 6000000:
            return 3
        elif salary > 2500000:
            return 2
        elif salary > 1500000:
            return 1
        else:
            return 0

    def year(s):
        return s[2:4]

    raw['Season'] = 25 - (((raw['Season'].apply(year)).astype(int)) + 4) % 100
    features = raw[used_col]
    features = features.to_numpy()
    lables = raw['salary'].apply(salary_level)
    lables = lables.to_list()

    model = tf.keras.models.load_model(
        'Q2/best_salary_model_acc=0.59.h5')
    prediction = model.predict(features)
    prediction = np.split(prediction, 11319)

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
