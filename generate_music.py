import sys
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from music21 import stream, note, chord

# Load trained model
model = load_model("output/music_model.h5")

# Load note mapping
with open("output/note_mapping.pkl", "rb") as file:
    note_to_int = pickle.load(file)

int_to_note = {value: key for key, value in note_to_int.items()}

# Generation settings
sequence_length = 50
num_notes = int(sys.argv[1]) if len(sys.argv) > 1 else 100

# Load original note sequence
with open("output/notes.pkl", "rb") as file:
    original_notes = pickle.load(file)

# Start from a random valid position
start = np.random.randint(0, len(original_notes) - sequence_length)
pattern = original_notes[start:start + sequence_length]

generated_notes = []

print("Generating music...")

for _ in range(num_notes):
    input_sequence = np.array(
        [[note_to_int[n] for n in pattern]]
    )

    input_sequence = input_sequence.reshape(1, sequence_length, 1)

    prediction = model.predict(input_sequence, verbose=0)
    index = np.argmax(prediction[0])

    result = int_to_note[index]

    generated_notes.append(result)

    pattern.append(result)
    pattern = pattern[1:]

# Create MIDI file
output = stream.Stream()

for item in generated_notes:
    if "." in item:
        pitches = [int(x) for x in item.split(".")]
        new_chord = chord.Chord(pitches)
        new_chord.quarterLength = 0.5
        output.append(new_chord)
    else:
        new_note = note.Note(item)
        new_note.quarterLength = 0.5
        output.append(new_note)

# Save generated music
output.write("midi", fp="output/generated_music.mid")

print("\nMusic generation complete!")
print("Saved to: output/generated_music.mid")