from pathlib import Path
import pickle
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Load preprocessed musical notes
with open("output/notes.pkl", "rb") as file:
    notes = pickle.load(file)

print(f"Total notes loaded: {len(notes)}")

# Create a unique vocabulary
unique_notes = sorted(set(notes))
note_to_int = {note: i for i, note in enumerate(unique_notes)}

print(f"Unique musical elements: {len(unique_notes)}")

# Create input sequences and target notes
sequence_length = 50
X = []
y = []

for i in range(len(notes) - sequence_length):
    sequence = notes[i:i + sequence_length]
    target = notes[i + sequence_length]

    X.append([note_to_int[n] for n in sequence])
    y.append(note_to_int[target])

X = np.array(X)
y = np.array(y)

print(f"Training sequences: {len(X)}")

# Build the LSTM model
model = Sequential([
    LSTM(128, input_shape=(sequence_length, 1), return_sequences=True),
    Dropout(0.2),
    LSTM(128),
    Dropout(0.2),
    Dense(len(unique_notes), activation="softmax")
])

model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer="adam"
)

# Reshape input for LSTM
X = X.reshape(X.shape[0], X.shape[1], 1)

# Train the model
print("\nStarting model training...")

model.fit(
    X,
    y,
    epochs=10,
    batch_size=64
)

# Create output folder
Path("output").mkdir(exist_ok=True)

# Save trained model
model.save("output/music_model.keras")

# Save vocabulary mappings
with open("output/note_mapping.pkl", "wb") as file:
    pickle.dump(note_to_int, file)

print("\nTraining complete!")
print("Model saved to: output/music_model.keras")
print("Note mapping saved to: output/note_mapping.pkl")