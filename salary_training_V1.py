import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split


def main():
    used_col = ['Season', 'age', 'team_w_pct', 'GP', 'w_pct', 'min/game', 'PTS/game', 'FG_pct',
                'FG3_pct', 'REB/game', 'AST/game', 'STL/game', 'BLK/game', 'TOV/game', 'Plus_Minus']
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
        """
        Returns the first two characters of the given str as a str.
        
        Assumes there are at least two characters in s.
        """
        return s[2:4]

    y = raw['salary'].apply(salary_level)
    df = raw[used_col]
    df['Season'] = 25 - (((df['Season'].apply(year)).astype(int)) + 4) % 100

    dftrain, dfeval, y_train, y_eval = train_test_split(df, y, test_size=0.2)

    def input_fn(features, labels, training=True, batch_size=256):
        # Convert the inputs to a Dataset.
        dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

        # Shuffle and repeat if you are in training mode.
        if training:
            dataset = dataset.shuffle(1000).repeat()
        
        return dataset.batch(batch_size)
    
    my_feature_columns = []
    for key in dftrain.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build a DNN with 2 hidden layers with 30 and 10 hidden nodes each.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 30 and 10 nodes respectively.
        hidden_units=[30, 10],
        # The model must choose between 3 classes.
        n_classes=15)

    classifier.train(
        input_fn=lambda: input_fn(dftrain, y_train, training=True),
        steps=10000)
    eval_result = classifier.evaluate(
        input_fn=lambda: input_fn(dfeval, y_eval, training=False))

    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))


if __name__ == '__main__':
    main()