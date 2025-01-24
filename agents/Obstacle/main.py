#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Obstacle
#  Created by Ingenuity i/o on 2025/01/24
#
#  Agent that display the bird on the Whiteboard depending of the pitch given


import sys
import ingescape as igs
import random

hautId = -1
basId = -1 #U.w.U

whiteboardWidth = 1000.0
whiteboardHeight = 1000.0

bmax = 60
bmin = 40

currentX = 1000.0
currentY = 500.0

obstacleNote = 50
note = 50

offset = 10

holeThickness = 200.0
obstacleThickness = 150.0

color = "#664566BA"

successfulAttempts = 0
nbAttempts = 0
localContact = False

def on_agent_event_callback(event, uuid, name, event_data, my_data):

    global whiteboardHeight, currentX

    if name == "Whiteboard":
        if event == igs.AGENT_KNOWS_US:

            pass   


#inputs
def input_callback(io_type, name, value_type, value, my_data):
    
    global whiteboardWidth, whiteboardHeight, bmin, bmax, obstacleNote, offset, note

    if(name == "whiteboardWidth"):
        whiteboardWidth = value
        print("whiteboardWidth set to : ", value)

    if(name == "whiteboardHeight"):
        whiteboardHeight = value
        print("whiteboardHeight set to : ", value)

    if(name == "bmax"):
        bmax = value
        print("bmax set to : ", value) 

    if(name == "bmin"):
        bmin = value
        print("bmin set to : ", value)
    
    if(name == "obstacleNote"):
        obstacleNote = value
        print("obstacleNote set to : ", value)

    if(name == "note"):
        note = value
        print("note set to : ", value)
    
    if(name == "offset"):
        offset = value
        print("offset set to : ", value)
       
       


def clock_callback(io_type, name, value_type, value, my_data):

    global currentX, currentY, obstacleThickness, bmin, bmax, color, note, obstacleNote, nbAttempts, successfulAttempts, localContact 

    epsilon = 2

    if(obstacleNote > bmin and obstacleNote < bmax):

        currentY = whiteboardHeight - (((obstacleNote - bmin) / (bmax - bmin)) * whiteboardHeight)

    # Check contact

    if(currentX < obstacleThickness and currentX > 0 and note > bmin and note < bmax):
    
        localContact = localContact or not(note < obstacleNote + epsilon and note > obstacleNote - epsilon)
  

    # Clear

    arguments_list = (hautId)
    igs.service_call("Whiteboard", "remove", arguments_list, "haut")

    arguments_list = (basId)
    igs.service_call("Whiteboard", "remove", arguments_list, "bas")

    # Draw again

    arguments_list = ("rectangle", currentX, 0.0, obstacleThickness, (currentY - (holeThickness / 2)), color, "transparent", 0)
    igs.service_call("Whiteboard", "addShape", arguments_list, "haut")

    arguments_list = ("rectangle", currentX, currentY + holeThickness / 2, obstacleThickness, whiteboardHeight - (currentY - (holeThickness / 2)), color, "transparent", 0)
    igs.service_call("Whiteboard", "addShape", arguments_list, "bas")

    currentX -= offset

    if(currentX < 0):

        currentX = whiteboardWidth

        nbAttempts += 1

        if(not(localContact)):
            successfulAttempts += 1

        successRate = str(successfulAttempts) + " / " + str(nbAttempts)

        arguments_list = (successRate)
        igs.service_call("Whiteboard", "setTitle", arguments_list, None)

        localContact = False

        # new note 

        # génère aléatoirement un entier entre bmin et bmax
        obstacleNote = random.randint(bmin, bmax)

    

    

def actionResult_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    pass

def elementCreated_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    
    global hautId, basId

    if(token == "haut"):
        hautId = arguments[0]
    
    if(token == "bas"):
        basId = arguments[0]

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_description("""<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Agent that display the bird on the Whiteboard depending of the pitch given</p></body></html>""")
    igs.definition_set_class("Obstacle")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    igs.input_create("whiteboardHeight", igs.INTEGER_T, None)
    igs.input_set_description("whiteboardHeight", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Height of the Whiteboard</p></body></html>""")
    igs.observe_input("whiteboardHeight", input_callback, None)
    igs.input_create("whiteboardWidth", igs.INTEGER_T, None)
    igs.input_set_description("whiteboardWidth", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Width of the Whiteboard</p></body></html>""")
    igs.observe_input("whiteboardWidth", input_callback, None)
    igs.input_create("bmax", igs.INTEGER_T, None)
    igs.input_set_description("bmax", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Maximum value of the note where the obstacle will be (correspond of the input of a MIDI keyboard)</p></body></html>""")
    igs.input_add_constraint("bmax", "range [0,127]")
    igs.observe_input("bmax", input_callback, None)
    igs.input_create("bmin", igs.INTEGER_T, None)
    igs.input_set_description("bmin", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Minimum value of the note where the obstacle will be (correspond of the input of a MIDI keyboard)</p></body></html>""")
    igs.input_add_constraint("bmin", "range [0,127]")
    igs.observe_input("bmin", input_callback, None)
    igs.input_create("offset", igs.INTEGER_T, None)
    igs.input_set_description("offset", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Size of the movement of the obstacle</p></body></html>""")
    igs.observe_input("offset", input_callback, None)
    igs.input_create("obstacleNote", igs.INTEGER_T, None)
    igs.input_set_description("obstacleNote", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Number of the note that wil determine the position of the obstacle on the screen (correspond of the input of a MIDI keyboard)</p></body></html>""")
    igs.input_add_constraint("obstacleNote", "range [0,127]")
    igs.observe_input("obstacleNote", input_callback, None)

    igs.input_create("note", igs.INTEGER_T, None)
    igs.input_add_constraint("note", "range [0,127]")
    igs.observe_input("note", input_callback, None)

    igs.input_create("clock", igs.IMPULSION_T, None)
    igs.input_set_description("clock", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Clock tick for the evolution of the obstacles</p></body></html>""")
    igs.observe_input("clock", clock_callback, None)

    igs.service_init("elementCreated", elementCreated_callback, None)
    igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)
    igs.service_init("actionResult", actionResult_callback, None)
    igs.service_arg_add("actionResult", "succeeded", igs.BOOL_T)

    igs.observe_agent_events(on_agent_event_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

