import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import TensorBoard, ReduceLROnPlateau
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.utils.class_weight import compute_class_weight
import pandas as pd
import numpy as np

# Loading data from the commands.csv file
file_path = "commands.csv"
data = pd.read_csv(file_path)

# Text, actions, and song preprocessing
texts = data['text'].values
actions = data['action'].values
songs = data['song'].fillna("").values

# Replacing empty songs with "unknown"
songs = ["unknown" if song == "" else song for song in songs]

# Handling rare songs
song_counts = pd.Series(songs).value_counts()
rare_threshold = 2  # Replace songs that occur less than two times with "other"
songs = [song if song_counts[song] >= rare_threshold else "other" for song in songs]

# Tokenization of the text
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
word_index = tokenizer.word_index

max_len = max(len(seq) for seq in sequences)
X = pad_sequences(sequences, maxlen=max_len, padding='post')

# Encoding actions
action_label_mapping = {"play": 0, "stop": 1}
y_actions = np.array([action_label_mapping[action] for action in actions])

# Tokenization of songs
song_tokenizer = Tokenizer()
song_tokenizer.fit_on_texts(songs)
song_vocab_size = len(song_tokenizer.word_index) + 1
y_songs = np.array([song_tokenizer.texts_to_sequences([song])[0][0] for song in songs])

# Building the model
vocab_size = len(word_index) + 1
embedding_dim = 128

# Input layer
input_text = Input(shape=(max_len,), name="input_text")

# Embedding and recurrent layers
x = Embedding(vocab_size, embedding_dim, input_length=max_len)(input_text)
x = Bidirectional(LSTM(128, return_sequences=True))(x)
x = Dropout(0.5)(x)
x = Bidirectional(LSTM(64))(x)

# Output for action classification
action_output = Dense(1, activation="sigmoid", name="action_output")(x)

# Output for song prediction
song_output = Dense(song_vocab_size, activation="softmax", name="song_output")(x)

# Setting loss weights
action_loss_weight = 2.0  # Higher value for more important task
song_loss_weight = 1.0    # Standard value

# Compiling the model
model = Model(inputs=input_text, outputs=[action_output, song_output])
model.compile(
    optimizer="adam",
    loss={
        "action_output": "binary_crossentropy",
        "song_output": "sparse_categorical_crossentropy"
    },
    metrics={
        "action_output": "accuracy",
        "song_output": "accuracy"
    },
    loss_weights={"action_output": action_loss_weight, "song_output": song_loss_weight}
)

# TensorBoard setup
tensorboard_callback = TensorBoard(log_dir="./logs", histogram_freq=1)

# Learning rate reduction on plateau
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-5)

# Training the model
history = model.fit(
    X,
    {"action_output": y_actions, "song_output": y_songs},
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    callbacks=[tensorboard_callback, reduce_lr]
)

# Saving the model
model.save("saved_model/music_action_model.h5")
print("Model saved to 'saved_model/music_action_model.h5'")