#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Switch
#  Created by Ingenuity i/o on 2025/01/25
#
#  Authors : Lucas Bolbènes, Armand Claveau, Priscilia Gonthier
#
#  Switch the input between the PitchDetector and the KeyBoard agents and return the output for the correct agent


import sys
import ingescape as igs

## Definition of global variables
# Switch input value
switch = "microphone"

# Callback function for the agent events
def on_agent_event_callback(event, uuid, name, event_data, my_data):

    global switch
    # When the agent is known by the Whiteboard agent, we display the input device in the chat
    if name == "Whiteboard":
        if event == igs.AGENT_KNOWS_US:
            arguments_list = ("Input device " + switch + " selected")
            igs.service_call("Whiteboard", "chat", arguments_list, None)

# Callback function to get and update the inputs from the other agents and set the output
def input_callback(io_type, name, value_type, value, my_data):
    global switch
    
    # Set the switch input value
    if (name == "switch"):
        switch = value
        # Display the switch on the whiteboard chat
        arguments_list = ("Switched to " + value + " input")
        igs.service_call("Whiteboard", "chat", arguments_list, None)
        print("switch set to : ", value)

    # Set the note output depending on the switch input value
    if (name == "pitchDetector" and switch == "microphone"):
        igs.output_set_int("note", value)
        print(name, " : ", value)
        pass

    if (name == "keyBoard" and switch == "keyboard"):
        igs.output_set_int("note", value)
        print(name, " : ", value)
        pass
    

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
    igs.definition_set_description("""<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Switch the input between the PitchDetector and the KeyBoard agents and return the output for the correct agent</p></body></html>""")
    igs.definition_set_class("Switch")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    ## Create the inputs of the agent
    igs.input_create("switch", igs.STRING_T, None)
    igs.input_set_description("switch", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Where to find the note (whether the microphone or the keyboard) </p></body></html>""")
    igs.observe_input("switch", input_callback, None)

    igs.input_create("pitchDetector", igs.INTEGER_T, None)
    igs.input_set_description("pitchDetector", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Number of the note found from the PitchDetector agent which correspond of the input of a MIDI keyboard</p></body></html>""")
    igs.input_add_constraint("pitchDetector", "range [0,127]")
    igs.observe_input("pitchDetector", input_callback, None)

    igs.input_create("keyBoard", igs.INTEGER_T, None)
    igs.input_set_description("keyBoard", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Number of the note found from the KeyBoard agent which correspond of the input of a MIDI keyboard</p></body></html>""")
    igs.input_add_constraint("keyBoard", "range [0,127]")
    igs.observe_input("keyBoard", input_callback, None)

    ## Create the output of the agent
    igs.output_create("note", igs.INTEGER_T, None)
    igs.output_set_description("note", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Number of the note from the PitchDetector agent or the KeyBoard agent which correspond of the input of a MIDI keyboard, depending on the switch input</p></body></html>""")

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

