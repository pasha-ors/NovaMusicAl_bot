import re
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

# Load the model
model_path = "neural_network/saved_model/music_action_model.h5"
model = load_model(model_path)
print(f"Model loaded from: {model_path}")

# Load data for the tokenizer
file_path = "neural_network/commands.csv"
data = pd.read_csv(file_path)
texts = data['text'].values

# Create the tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
word_index = tokenizer.word_index

# Set the maximum sequence length
max_len = max(len(seq) for seq in tokenizer.texts_to_sequences(texts))

# Regular expression to extract song title
def extract_song_with_regex(text):
    # Regular expression to find structure "play <song> by <artist>"
    match = re.search(r"play (.+?) by (.+)", text, re.IGNORECASE)
    if match:
        return match.group(1)  # Return song title
    # If no "by" structure, look for just "play <song>"
    match = re.search(r"play (.+)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    return ""

# Function to classify action and extract song title
def classify_action_and_extract_song(text):
    # Convert text to numerical sequence for the model
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')

    # Classify action
    predictions = model.predict(padded_sequence)
    action_pred = predictions[0].ravel()  # Action prediction
    action_label = "stop" if action_pred[0] > 0.5 else "play"

    # Extract song title
    song_name = extract_song_with_regex(text)

    return action_label, song_name
