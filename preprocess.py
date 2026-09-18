from pathlib import Path
import pickle
from music21 import converter, note, chord

# Folder containing our MIDI dataset
midi_folder = Path("midi_data")

# File where extracted note sequences will be saved
output_file = Path("output/notes.pkl")

notes = []

# Process every MIDI file
for midi_file in sorted(midi_folder.glob("*.mid")):
    try:
        print(f"Processing: {midi_file.name}")

        # Load the MIDI file
        midi = converter.parse(midi_file)

        # Extract notes and chords
        for element in midi.flatten().notes:

            if isinstance(element, note.Note):
                notes.append(str(element.pitch))

            elif isinstance(element, chord.Chord):
                notes.append(".".join(str(n) for n in element.normalOrder))

    except Exception as error:
        print(f"Skipped {midi_file.name}: {error}")

# Save the extracted sequence
with open(output_file, "wb") as file:
    pickle.dump(notes, file)

print(f"\nPreprocessing complete!")
print(f"Total musical elements extracted: {len(notes)}")
print(f"Saved to: {output_file}")