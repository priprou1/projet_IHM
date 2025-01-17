#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Obstacle
#  Created by Ingenuity i/o on 2025/01/10
#
# no description


import sys
import ingescape as igs

hautId = -1
basId = -1 #U.w.U

whiteboardWidth = 1000.0
whiteboardHeight = 1000.0

bmax = 60
bmin = 40

currentX = 1000.0
currentY = 500.0

note = 50

offset = 10

holeThickness = 200.0
obstacleThickness = 150.0

color = "#664566BA"

def on_agent_event_callback(event, uuid, name, event_data, my_data):

    global whiteboardHeight, currentX

    if name == "Whiteboard":
        if event == igs.AGENT_KNOWS_US:

            pass   


#inputs
def input_callback(io_type, name, value_type, value, my_data):
    
    global whiteboardWidth, whiteboardHeight, bmin, bmax, note, offset

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
    
    if(name == "note"):
        note = value
        print("note set to : ", value)
    
    if(name == "offset"):
        offset = value
        print("offset set to : ", value)
       


def clock_callback(io_type, name, value_type, value, my_data):

    global currentX, currentY, obstacleThickness, bmin, bmax, color

    if(note > bmin and note < bmax):

        currentY = whiteboardHeight - (((note - bmin) / (bmax - bmin)) * whiteboardHeight)

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
    igs.definition_set_class("Obstacle")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    igs.input_create("whiteboardHeight", igs.INTEGER_T, None)
    igs.observe_input("whiteboardHeight", input_callback, None)

    igs.input_create("note", igs.INTEGER_T, None)
    igs.observe_input("note", input_callback, None)

    igs.input_create("clock", igs.IMPULSION_T, None)
    igs.observe_input("clock", clock_callback, None)

    igs.input_create("bmin", igs.INTEGER_T, None)
    igs.observe_input("bmin", input_callback, None)

    igs.input_create("bmax", igs.INTEGER_T, None)
    igs.observe_input("bmax", input_callback, None)

    igs.input_create("offset", igs.INTEGER_T, None)
    igs.observe_input("offset", input_callback, None)

    igs.service_init("elementCreated", elementCreated_callback, None)
    igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)

    igs.service_init("actionResult", actionResult_callback, None)
    igs.service_arg_add("actionResult", "succeeded", igs.BOOL_T)

    igs.observe_agent_events(on_agent_event_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

