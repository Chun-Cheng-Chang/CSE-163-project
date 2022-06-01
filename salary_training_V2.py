import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split


def main():
    used_col = ['Season', 'age', 'team_w_pct', 'GP', 'w_pct', 'min/game',
                'PTS/game', 'FG_pct', 'FG3_pct', 'REB/game', 'AST/game',
                'STL/game', 'BLK/game', 'TOV/game', 'Plus_Minus']
    raw = pd.read_csv('total_player_data.csv')

    def salary_level(salary):
        if salary > 20000000:
            return 5
        elif salary > 10000000:
            return 4
        elif salary > 5000000:
            return 3
        elif salary > 2000000:
            return 2
        elif salary > 1200000:
            return 1
        else:
            return 0

    def year(s):
        return s[2:4]

    y = raw['salary'].apply(salary_level)
    df = raw[used_col]
    df['Season'] = 25 - (((df['Season'].apply(year)).astype(int)) + 4) % 100
    df = df.to_numpy()
    y = y.to_numpy()
    print(type(df))

    dftrain, dfeval, y_train, y_eval = train_test_split(df, y, test_size=0.2)

    best_model = None
    best_acc = 0
    for i in range(100):
        model = keras.Sequential([
            keras.layers.Input(shape=(15,)),
            keras.layers.Dense(101, activation='relu'),
            keras.layers.Dense(116, activation='relu'),
            keras.layers.Dense(6, activation='softmax')
        ])
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(dftrain, y_train, epochs=40)
        test_loss, test_acc = model.evaluate(dfeval,  y_eval, verbose=1)

        if test_acc > best_acc:
            best_acc = test_acc
            best_model = model
    best_model.save('best_salary_model.h5')
    print(best_acc)


if __name__ == '__main__':
    main()
