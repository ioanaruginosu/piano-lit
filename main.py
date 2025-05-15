# import time
# import pygame
# import pretty_midi
# import mido
# import cv2
# import numpy as np
# import threading
# from gtts import gTTS
# import os
# from flask import Flask, jsonify, render_template
# from queue import Queue
# from playsound import playsound
# import datetime
#
# app = Flask(__name__)
#
# ########################################
# #               MIDI LOGIC
# ########################################
#
# def load_midi_notes(midi_file):
#     """Extract notes from a MIDI file."""
#     midi_data = pretty_midi.PrettyMIDI(midi_file)
#     song_notes = []
#     for instrument in midi_data.instruments:
#         if not instrument.is_drum:  # Skip drum tracks
#             for note in instrument.notes:
#                 song_notes.append({
#                     "note": pretty_midi.note_number_to_name(note.pitch),
#                     "midi": note.pitch,
#                     "start_time": note.start,
#                     "duration": note.end - note.start,
#                 })
#     return sorted(song_notes, key=lambda x: x["start_time"])
#
#
# ########################################
# #        PYGAME VISUALIZATION SETUP
# ########################################
#
# pygame.init()
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 300
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("MIDI Visualization")
#
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)
#
# note_range = range(48, 85)
# key_width = SCREEN_WIDTH // len(note_range)
#
# def is_black_key(note):
#     NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
#     return NOTE_NAMES[note % 12] in ['C#', 'D#', 'F#', 'G#', 'A#']
#
# keys = []
# for i, note in enumerate(note_range):
#     x = i * key_width
#     keys.append({
#         "rect": pygame.Rect(x, 50, key_width, 200),
#         "note": note,
#         "color": BLACK if is_black_key(note) else WHITE,
#         "status": None,
#         "status_time": None,
#     })
#
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fps = 2.5
# timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# video_filename = f"midi_visualization_{timestamp}.avi"
#
# out = cv2.VideoWriter(video_filename, fourcc, fps, (SCREEN_WIDTH, SCREEN_HEIGHT))
#
# def draw_keys():
#     screen.fill(WHITE)
#     current_time = time.time()
#     for key in keys:
#         if key["status_time"] and current_time - key["status_time"] > 0.3:
#             key["status"] = None
#             key["status_time"] = None
#
#         color = key["color"]
#         if key["status"] is True:
#             color = GREEN
#         elif key["status"] is False:
#             color = RED
#         elif key["status"] == "off_beat":
#             color = YELLOW
#
#         pygame.draw.rect(screen, color, key["rect"])
#         pygame.draw.rect(screen, BLACK, key["rect"], 2)
#
#     pygame.display.flip()
#     capture_screen()
#
# def capture_screen():
#     frame = pygame.surfarray.array3d(pygame.display.get_surface())
#     frame = cv2.cvtColor(np.rot90(frame), cv2.COLOR_RGB2BGR)
#     out.write(frame)
#
# ########################################
# #           VOICE ASSISTANT
# ########################################
#
# def speak(text):
#     tts = gTTS(text)
#     tts.save("temp_voice.mp3")
#     playsound("temp_voice.mp3")
#
# ########################################
# #    REAL-TIME MIDI RECORDING LOGIC
# ########################################
#
# def record_midi_input(expected_notes):
#     played_notes = []
#     start_time = "none"
#
#     correct_count = 0
#     incorrect_count = 0
#     tolerance = 0.7
#     extra_time = 0
#
#     correct = 0
#     incorrect = 0
#     off_beat = 0
#     total = 0
#
#     print("Listening for MIDI input... Please play the song!")
#     draw_keys()
#
#     with mido.open_input() as input_port:
#         while len(played_notes) < len(expected_notes):
#             for message in input_port.iter_pending():
#                 if message.type == 'note_on' and message.velocity > 0:
#                     if start_time == "none":
#                         start_time = time.time()
#                     elapsed_time = time.time() - start_time
#                     midi_note = message.note
#                     played_notes.append({
#                         "midi": midi_note,
#                         "start_time": elapsed_time
#                     })
#                     note_index = len(played_notes) - 1
#                     is_correct = note_index < len(expected_notes) and expected_notes[note_index]["midi"] == midi_note
#                     if is_correct:
#                         if abs(expected_notes[note_index]["start_time"] - elapsed_time) > (tolerance + extra_time):
#                             extra_time = abs(expected_notes[note_index]["start_time"] - elapsed_time)
#                             is_correct = "off_beat"
#
#                     total += 1
#                     if is_correct is True:
#                         extra_time = 0
#                         correct_count += 1
#                         correct += 1
#                         if correct_count == 12:
#                             threading.Thread(target=speak, args=("Good job",)).start()
#                         if correct_count == 30:
#                             threading.Thread(target=speak, args=("Keep it up",)).start()
#                     else:
#                         incorrect_count += 1
#                         if is_correct is False:
#                             incorrect += 1
#                         else:
#                             off_beat += 1
#                         correct_count = 0
#                         if incorrect_count == 7:
#                             threading.Thread(target=speak, args=("Watch out for the LEDs",)).start()
#
#                     if note_index == 0:
#                         is_correct = True
#
#                     for key in keys:
#                         if key["note"] == midi_note:
#                             key["status"] = is_correct
#                             key["status_time"] = time.time()
#
#                     draw_keys()
#                     time.sleep(0.02)
#         accuracy = ((correct + off_beat) / total) * 100 if total > 0 else 0
#         return played_notes, correct, incorrect, off_beat, accuracy
#
# ########################################
# #           FLASK ROUTES
# ########################################
#
# @app.route('/')
# @app.route('/statistics')
# def statistics():
#     return render_template('frame1.html')
#
# @app.route('/accomplishments')
# def accomplishments():
#     return render_template('frame2.html')
#
# @app.route('/songs-history')
# def songs_history():
#     return render_template('frame3.html')
#
# @app.route('/api/results', methods=['GET'])
# def get_results():
#     expected_file = "Twinkle_Twinkle_Right_RIGHT.mid"
#     expected_notes = load_midi_notes(expected_file)
#     played_notes, correct, incorrect, off_beat, accuracy = record_midi_input(expected_notes)
#
#     out.release()
#     return jsonify({
#         "correct_notes": correct,
#         "incorrect_notes": incorrect,
#         "off_time_notes": off_beat,
#         "accuracy": accuracy
#     })
#
# if __name__ == "__main__":
#     app.run(debug=True, threaded=True)