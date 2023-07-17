import tensorflow as tf
import keras as keras
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras import Sequential
from keras.layers import Dense, Embedding, Dropout, LSTM
import pandas as pd

df = pd.read_csv('data/data.csv')
df['comment'] = df['comment'].apply(str)

train_features = df['comment']
train_labels = df['toxic']

vocab_size = 20000
max_seq_len = 20
vector_size = 300

tokenizer = Tokenizer(oov_token="<OOV>", num_words=vocab_size)
tokenizer.fit_on_texts(train_features)
sequences_train = tokenizer.texts_to_sequences(train_features)
padded_train = pad_sequences(sequences_train, padding='post', maxlen=max_seq_len)

def get_model():
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=vector_size, input_length=max_seq_len))
    model.add(Dropout(0.6))
    model.add(LSTM(max_seq_len, return_sequences=True))
    model.add(LSTM(6))
    model.add(Dense(1, activation='sigmoid'))
    return model


callbacks = [
    keras.callbacks.EarlyStopping(  # type: ignore
      monitor="val_loss", patience=2, verbose=1, mode="min", restore_best_weights=True
    ),
]

model = get_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

tf.config.run_functions_eagerly(True)
history = model.fit(padded_train, train_labels, validation_split=0.33, callbacks=callbacks, epochs=10)
