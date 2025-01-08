#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Bird
#  Created by Ingenuity i/o on 2025/01/04
#
# no description


import sys
import ingescape as igs

id = -1

def on_agent_event_callback(event, uuid, name, event_data, my_data):
    if name == "Whiteboard":
        if event == igs.AGENT_KNOWS_US:
            # igs.service_call(uuid, "getElements", None, "bird")
            # arguments_list = ("rectangle", 50.0, 50.0, 50.0, 50.0, "blue", "transparent", 0)
            # igs.service_call("Whiteboard", "addShape", arguments_list, "bird")

            arguments_list = ("https://raw.githubusercontent.com/priprou1/projet_IHM/refs/heads/master/Bird.png", 20.0, 20.0)
            igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, "bird")

        elif event == igs.AGENT_EXITED:
            pass


def actionResult_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    # print("succeed ? : ", arguments[0])
    pass

def elementCreated_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    
    global id

    if(token == "bird"):
        id = arguments[0]
        print(id)

def input_callback(io_type, name, value_type, value, my_data):

    # On suppose que les notes pertinentes sont celles de 20 à 100
    # On suppose que la hauteur du whiteboard est de 0 à 680

    global id

    bmin = 40
    bmax = 84

    screen_height = 1000

    if(value > bmin and value < bmax):

        height = screen_height - (((value - bmin) / (bmax - bmin)) * screen_height)

        print(value, " ; ", height)

        if(id != -1):
            arguments_list = (id, 50.0, height)
            igs.service_call("Whiteboard", "moveTo", arguments_list, "")
        
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_class("Bird")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    igs.input_create("note", igs.INTEGER_T, None)
    igs.observe_input("note", input_callback, None)

    igs.service_init("elementCreated", elementCreated_callback, None)
    igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)

    igs.service_init("actionResult", actionResult_callback, None)
    igs.service_arg_add("actionResult", "succeeded", igs.BOOL_T)


    igs.observe_agent_events(on_agent_event_callback, None)


    igs.start_with_device(sys.argv[2], int(sys.argv[3]))
    
   
    input()

    igs.stop()

