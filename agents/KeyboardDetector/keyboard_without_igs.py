import sys
import os
# Add the keyboard directory to the path in order to import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from modules import midiConverter as mc
import tkinter as tk

# Constants
WHITE_KEYS = ["C", "D", "E", "F", "G", "A", "B"]
KEY_COLORS = {"white": "white", "black": "black"}
KEY_WIDTH = 30
KEY_HEIGHT = 150
BLACK_KEY_WIDTH = 20
BLACK_KEY_HEIGHT = 100
OCTAVES = 5
START_OCTAVE = 2
OFFSET = 25
KEYBOARD_HEIGHT = KEY_HEIGHT + OFFSET
KEYBOARD_WIDTH = len(WHITE_KEYS) * KEY_WIDTH * OCTAVES + 2 * OFFSET

# Display the note and play it
def play_note(note, octave):
    midiNumber = mc.string_to_midi(note + str(octave))
    print(f"Playing note: {note}{octave}, MIDI number: {midiNumber}")

# Main window
keyboard = tk.Tk()
keyboard.title("Piano MIDI Keyboard")
keyboard.geometry(f"{KEYBOARD_WIDTH}x{KEYBOARD_HEIGHT}")

# Canvas to draw the keyboard
canvas = tk.Canvas(keyboard, width=KEYBOARD_WIDTH, heigh=KEYBOARD_HEIGHT, bg="gray")
canvas.pack()

# Draw white keys
white_key_positions = []
for i in range(len(WHITE_KEYS) * OCTAVES):
    x = i * KEY_WIDTH
    key = canvas.create_rectangle(x + OFFSET , 0, x + OFFSET + KEY_WIDTH, KEY_HEIGHT, fill=KEY_COLORS["white"], outline="black")
    canvas.tag_bind(key, "<Button-1>", lambda e, note=WHITE_KEYS[i % len(WHITE_KEYS)], octave=(i // len(WHITE_KEYS)) + START_OCTAVE : play_note(note, octave))
    white_key_positions.append(x)

# Draw black keys
for i in range(len(WHITE_KEYS) * OCTAVES - 1):  # No Black keys after E and B
    if i % len(WHITE_KEYS) in [2, 6]:  # Jump spaces between E-F and B-C
        continue
    x = white_key_positions[i] + (KEY_WIDTH - BLACK_KEY_WIDTH // 2)
    key = canvas.create_rectangle(x + OFFSET, 0, x + OFFSET + BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT, fill=KEY_COLORS["black"], outline="black")
    canvas.tag_bind(key, "<Button-1>", lambda e, note=WHITE_KEYS[i % len(WHITE_KEYS)] + "#", octave=(i // len(WHITE_KEYS)) + START_OCTAVE : play_note(note, octave))

# Add labels to the first and last keys
canvas.create_text(KEY_WIDTH // 2 + OFFSET, KEY_HEIGHT + 10, text=f"{WHITE_KEYS[0]}{START_OCTAVE}", font=("Arial", 10), fill="black")
canvas.create_text(KEYBOARD_WIDTH - KEY_WIDTH // 2 - OFFSET, KEY_HEIGHT + 10, text=f"{WHITE_KEYS[-1]}{OCTAVES + START_OCTAVE - 1}", font=("Arial", 10), fill="black")

# Launch application
keyboard.mainloop()