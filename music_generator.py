from pathlib import Path
from music21 import corpus, converter

# Folder where MIDI files will be stored
output_folder = Path("midi_data")
output_folder.mkdir(exist_ok=True)

count = 0

# Get all files from the music21 core corpus
score_files = corpus.getCorePaths()

for file_path in score_files:
    # Process only XML and MXL music files
    if file_path.suffix.lower() not in [".xml", ".mxl"]:
        continue

    try:
        # Read the musical score
        score = converter.parse(file_path)

        # Create MIDI filename
        midi_name = f"music_{count + 1}.mid"
        destination = output_folder / midi_name

        # Convert the score to MIDI
        score.write("midi", fp=destination)

        count += 1
        print(f"Created MIDI: {midi_name}")

        # Keep the dataset manageable
        if count >= 50:
            break

    except Exception as error:
        print(f"Skipped {file_path.name}: {error}")

print(f"\nDataset collection complete: {count} MIDI files")