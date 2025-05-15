# generate_sheet.py
from music21 import converter, environment

us = environment.UserSettings()
us['musicxmlPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
us['musescoreDirectPNGPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'

# 1. Load your MIDI file
midi_path = 'Twinkle_Twinkle_Right_RIGHT.mid'
score = converter.parse(midi_path)

# 2. (Optional) tweak layout, transpose, pick parts…
#    e.g. score = score.transpose(0)
#         score = score.parts[0]

# 3. Write out a PNG (via MusicXML + MuseScore)
png_path = score.write('musicxml.png')

print(f'Sheet music image written to: {png_path}')
