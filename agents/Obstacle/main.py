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
screenHeight = 1000.0
bmin = -1
bmax = -1

currentX = 1000.0

currentY = 0.0

holeThickness = 100.0

def on_agent_event_callback(event, uuid, name, event_data, my_data):

    global screenHeight, currentX

    if name == "Whiteboard":
        if event == igs.AGENT_KNOWS_US:

            thickness = 100.0

            arguments_list = ("rectangle", currentX, 0.0, thickness, 500.0, "blue", "transparent", 0)
            igs.service_call("Whiteboard", "addShape", arguments_list, "haut")

            arguments_list = ("rectangle", currentX, 550.0, thickness, 500.0, "blue", "transparent", 0)
            igs.service_call("Whiteboard", "addShape", arguments_list, "bas")


#inputs
def input_callback(io_type, name, value_type, value, my_data):
    
    global screenHeight

    if(name == "screenHeight"):
        screenHeight = value
        print("screenHeight set to : ", value)

    if(name == "bmin"):
        bmin = value
        print("bmin set to : ", value)
    
    if(name == "bmax"):
        bmax = value
        print("bmax set to : ", value)    


def clock_callback(io_type, name, value_type, value, my_data):

    global currentX

    arguments_list = (hautId, -10.0, 0.0)
    igs.service_call("Whiteboard", "translate", arguments_list, "haut")

    arguments_list = (basId, -10.0, 0.0)
    igs.service_call("Whiteboard", "translate", arguments_list, "bas")

    currentX -= 10.0   

    if(currentX < 0):

        currentX = 1000.0

        arguments_list = (hautId, currentX, 0.0)
        igs.service_call("Whiteboard", "moveTo", arguments_list, "haut")

        arguments_list = (basId, currentX, 550.0)
        igs.service_call("Whiteboard", "moveTo", arguments_list, "bas")

    

def actionResult_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    pass

def elementCreated_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    
    global hautId, basId

    if(token == "haut"):
        hautId = arguments[0]
        print(hautId)   
    
    if(token == "bas"):
        basId = arguments[0]
        print(basId)


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

    igs.input_create("screenHeight", igs.INTEGER_T, None)
    igs.observe_input("screenHeight", input_callback, None)

    igs.input_create("note", igs.INTEGER_T, None)
    igs.observe_input("note", input_callback, None)

    igs.input_create("clock", igs.IMPULSION_T, None)
    igs.observe_input("clock", clock_callback, None)

    igs.service_init("elementCreated", elementCreated_callback, None)
    igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)

    igs.service_init("actionResult", actionResult_callback, None)
    igs.service_arg_add("actionResult", "succeeded", igs.BOOL_T)

    igs.input_create("bmin", igs.INTEGER_T, None)
    igs.observe_input("bmin", input_callback, None)

    igs.input_create("bmax", igs.INTEGER_T, None)
    igs.observe_input("bmax", input_callback, None)

    igs.observe_agent_events(on_agent_event_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

