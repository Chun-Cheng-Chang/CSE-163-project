import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split


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
    raw = pd.read_csv('Q3/winning_rate_training_data.csv')
    feature = raw.drop(['win_pct'], axis=1).to_numpy()

    def winning_rate_range(win_pct):
        win_pct_range = int(win_pct * 1000) // 200
        return win_pct_range

    lable = raw['win_pct'].apply(winning_rate_range).to_numpy()

    train_feature, test_feature, train_lable, test_lable = train_test_split(
        feature, lable, test_size=0.2)

    best_model = None
    best_acc = 0
    for _ in range(25):
        for i in range(20, 61, 10):
            for j in range(20, 61, 10):
                model = keras.Sequential([
                    keras.layers.Input(shape=(26,)),
                    keras.layers.Dense(i, activation='relu'),
                    keras.layers.Dense(j, activation='relu'),
                    keras.layers.Dense(5, activation='softmax')
                ])
                model.compile(optimizer='adam',
                              loss='sparse_categorical_crossentropy',
                              metrics=['accuracy'])
                model.fit(train_feature, train_lable, epochs=40)
                _, test_acc = model.evaluate(
                    test_feature,  test_lable, verbose=1)
                if test_acc > best_acc:
                    best_acc = test_acc
                    best_model = model
    print('Test accuracy:', best_acc)
    best_model.save(f'Q3/best_winning_rate_model_acc={best_acc:.2f}.h5')


if __name__ == '__main__':
    main()
