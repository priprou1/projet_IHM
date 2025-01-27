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

# Function to get the current note from the keyboard
def get_current_note():
    app = tk.Tk()
    app.bind("<Return>", on_enter)
    app.mainloop()

    # while True:

    #     try:
    #         # Prompt user for input
    #         note_string = input("Enter a musical note (e.g., C4, D#-1): ").strip()
            
    #         # Convert to MIDI number
    #         midi_number = mc.string_to_midi(note_string)
            
    #         # Display the result
    #         print(f"{note_string} : {midi_number}")
    #         # Return the MIDI number
    #         igs.output_set_int("note", midi_number)

    #     except ValueError as e:
    #         # Handle invalid input
    #         print(f"Invalid input: {e}. Please try again.")

    #     except KeyboardInterrupt:
    #         # Exit on Ctrl+C
    #         print('Interrupt')
    #         break
    pass

def on_enter_callback(event):

    


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

