#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Bird
#  Created by Ingenuity i/o on 2025/01/24
#
#  Authors : Lucas Bolbènes, Armand Claveau, Priscilia Gonthier
#
#  Agent that display the bird on the Whiteboard depending of the pitch given


import sys
import ingescape as igs

## Definition of global variables
# ID of the bird on the whiteboard
id = -1
# Height of the whiteboard
whiteboardHeight = 1000.0
# Minimum and maximum values of the note that the bird can reach
bmin = 40
bmax = 60
# Size of the bird
birdSize = 150.0

# Callback function for the agent events
def on_agent_event_callback(event, uuid, name, event_data, my_data):
    if name == "Whiteboard":
        # When the agent is known by the Whiteboard agent, we add the image of the bird on the whiteboard
        if event == igs.AGENT_KNOWS_US:
            arguments_list = ("https://raw.githubusercontent.com/priprou1/projet_IHM/refs/heads/master/Bird.png", 20.0, 20.0)
            igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, "bird")
        # TODO : Sert à quoi? fait quelque chose? Si oui à commenter sinon à supprimer
        elif event == igs.AGENT_EXITED:
            pass

# TODO : Elle fait quoi cette fonction? Ne sert à rien non ? Peut-elle être supprimée ? Sinon la commenter
def actionResult_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    pass

# Callback function to get the ID of the bird on the whiteboard
def elementCreated_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    
    global id

    if(token == "bird"):
        id = arguments[0]
        print(id)

# Callback function to get and update the inputs from the other agents
def input_callback(io_type, name, value_type, value, my_data):
    
    global bmin, bmax, whiteboardHeight

    if(name == "bmin"):
        bmin = value
        print("bmin set to : ", value)

    if(name == "bmax"):
        bmax = value
        print("bmax set to : ", value)

    if(name == "whiteboardHeight"):
        whiteboardHeight = value
        print("whiteboardHeight set to : ", value)

# Callback function to get the note input and move the bird on the whiteboard accordingly
def note_input_callback(io_type, name, value_type, value, my_data):

    global id, bmin, bmax, whiteboardHeight, birdSize

    if(value > bmin and value < bmax):

        currentY = whiteboardHeight - (((value - bmin) / (bmax - bmin)) * whiteboardHeight)

        # Print the value of the note and the current position of the bird in the console for debugging #TODO : A laisser ou pas?
        print(value, " ; ", currentY)

        if(id != -1):
            arguments_list = (id, 50.0, currentY - (birdSize / 2))
            igs.service_call("Whiteboard", "moveTo", arguments_list, "")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    # Set the documentation of the agent
    igs.agent_set_name(sys.argv[1])
    igs.definition_set_description("""<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Agent that display the bird on the Whiteboard depending of the pitch given</p></body></html>""")
    igs.definition_set_class("Bird")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    ## Create the inputs of the agent
    igs.input_create("whiteboardHeight", igs.INTEGER_T, None)
    igs.input_set_description("whiteboardHeight", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Height of the Whiteboard</p></body></html>""")
    igs.observe_input("whiteboardHeight", input_callback, None)

    igs.input_create("bmax", igs.INTEGER_T, None)
    igs.input_set_description("bmax", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Maximum value of the note that the bird can reach (correspond of the input of a MIDI keyboard)</p></body></html>""")
    igs.input_add_constraint("bmax", "range [0,127]")
    igs.observe_input("bmax", input_callback, None)

    igs.input_create("bmin", igs.INTEGER_T, None)
    igs.input_set_description("bmin", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Minimum value of the note that the bird can reach (correspond of the input of a MIDI keyboard)</p></body></html>""")
    igs.input_add_constraint("bmin", "range [0,127]")
    igs.observe_input("bmin", input_callback, None)

    igs.input_create("note", igs.INTEGER_T, None)
    igs.input_set_description("note", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Number of the note that will determine the position of the bird on the screen (correspond of the input of a MIDI keyboard)</p></body></html>""")
    igs.input_add_constraint("note", "range [0,127]")
    igs.observe_input("note", note_input_callback, None)
    
    ## Initialise the services of the agent
    igs.service_init("elementCreated", elementCreated_callback, None)
    igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)
    # TODO : A quoi sert cette fonction? Peut-elle être supprimée? Sinon la commenter
    igs.service_init("actionResult", actionResult_callback, None)
    igs.service_arg_add("actionResult", "succeeded", igs.BOOL_T)

    igs.observe_agent_events(on_agent_event_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))
   
    input()

    igs.stop()

