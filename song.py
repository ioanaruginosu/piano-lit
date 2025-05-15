import pretty_midi

# Load the MIDI file
midi_data = pretty_midi.PrettyMIDI("twinklestar.mid")

# Extract notes from the first instrument
notes = []
for instrument in midi_data.instruments:
    if not instrument.is_drum:  # Ignore drums
        for note in instrument.notes:
            notes.append({
                "note": pretty_midi.note_number_to_name(note.pitch),
                "start_time": note.start,
                "duration": note.end - note.start
            })

# Print the extracted notes
for note in notes:
    print(note)
