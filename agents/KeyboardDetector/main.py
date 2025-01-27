#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  KeyboardDetector
#  Created by Ingenuity i/o on 2025/01/27
#
#  Authors : Lucas Bolbènes, Armand Claveau, Priscilia Gonthier
#
#  Agent that detect the note from the input of the keyboard


import sys
import os
# Add the root directory to the path in order to import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import ingescape as igs
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
KEYBOARD_HEIGHT = KEY_HEIGHT + offset
KEYBOARD_WIDTH = len(WHITE_KEYS) * KEY_WIDTH * OCTAVES + 2 * offset

# Function to get the current note from the keyboard
def get_current_note():
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

# Display the note and return it
def play_note(note, octave):
    midiNumber = mc.string_to_midi(note + str(octave))
    print(f"Playing note: {note}{octave}, MIDI number: {midiNumber}")
    igs.output_set_int("note", midiNumber)



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)


    ## Set the documentation of the agent
    igs.agent_set_name(sys.argv[1])
    igs.definition_set_description("""<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Agent that detect the note from the input of the keyboard</p></body></html>""")
    igs.definition_set_class("KeyboardDetector")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    ## Create the output of the agent
    igs.output_create("note", igs.INTEGER_T, None)
    igs.output_set_description("note", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Number of the note found wich correspond of the input of a MIDI keyboard</p></body></html>""")
    igs.output_add_constraint("note", "range [0,127]")

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    get_current_note()

    igs.stop()

