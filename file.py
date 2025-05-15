# from mido import Message, MidiFile, MidiTrack
#
# # Create a new MIDI file and track
# midi = MidiFile()
# track = MidiTrack()
# midi.tracks.append(track)
#
# # Corrected notes with their respective durations (quarter notes)
# notes = [
#     ("C4", 480)
# ]
#
# # Mapping note names to MIDI numbers
# note_mapping = {
#     "C4": 60
# }
#
# # Add notes to the track
# for note, duration in notes:
#     midi_note = note_mapping[note]
#     track.append(Message('note_on', note=midi_note, velocity=64, time=0))
#     track.append(Message('note_off', note=midi_note, velocity=64, time=duration))
#
# # Save the MIDI file
# output_path = "test.mid"
# midi.save(output_path)
# print(f"MIDI file saved as {output_path}")
