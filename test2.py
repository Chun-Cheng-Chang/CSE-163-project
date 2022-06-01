import tensorflow as tf

new_model = tf.keras.models.load_model('best_salary_model_V2.h5')

print(new_model.summary())