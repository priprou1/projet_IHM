#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  PitchDetector
#  Created by Ingenuity i/o on 2025/01/04
#
#  Authors : Lucas Bolbènes, Armand Claveau, Priscilia Gonthier
#
#  Agent that detect the pitch from the voice input of the microphone


import sys
import ingescape as igs

import aubio
import numpy as np
import pyaudio
import time
import argparse
import queue
import music21  

## Definition of global variables
# Threshold of the volume capture by the microphone in order to reduce the unwanted noise
VOLUME_TRESH = 0.2
SILENCE_TRESH = -40
# Number of the device used for the microphone
DEVICE_NUMBER = 9

# Callback function to get and update the inputs from the other agents
def input_callback(io_type, name, value_type, value, my_data):

    global VOLUME_TRESH

    if(name == "volumeTresh"):
        VOLUME_TRESH = value
        print("Volume treshold set to : ", value)

# Function to get the current note from the microphone #TODO : Code à commenter dedans ou pas, à voir
def get_current_note(printOut=False):

    global VOLUME_TRESH

    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print("Device number (%i): %s" % (i, p.get_device_info_by_index(i).get('name')))

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, input=True,
                    input_device_index=DEVICE_NUMBER, frames_per_buffer=4096)

    time.sleep(1)

    pDetection = aubio.pitch("default", 2048, 2048//2, 44100)
    pDetection.set_unit("Hz")
    pDetection.set_silence(SILENCE_TRESH)

    q = queue.Queue()

    current_pitch = music21.pitch.Pitch()

    try:
        while True:

            data = stream.read(1024, exception_on_overflow=False)
            samples = np.fromstring(data,
                                    dtype=aubio.float_type)
            pitch = pDetection(samples)[0]

            volume = np.sum(samples**2)/len(samples) * 100

            if pitch and volume > VOLUME_TRESH:  
                current_pitch.frequency = pitch
            else:
                continue

            if printOut:
                print(current_pitch, " : ", current_pitch.nameWithOctave)
                igs.output_set_int("note", current_pitch.midi)

            else:
                current = current_pitch.nameWithOctave
                q.put({'Note': current, 'Cents': current_pitch.microtone.cents})

    except KeyboardInterrupt:
        print('Interrupt')
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

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
    igs.definition_set_description("""<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Agent that detect the pitch from the voice input of the microphone</p></body></html>""")
    igs.definition_set_class("PitchDetector")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    ## Create the inputs of the agent
    igs.input_create("volumeTresh", igs.DOUBLE_T, None)
    igs.input_set_description("volumeTresh", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Threshold of the volume capture by the microphone in order to reduice the unwanted noise</p></body></html>""")
    igs.input_add_constraint("volumeTresh", "range [0.01,1]")
    igs.observe_input("volumeTresh", input_callback, None)

    ## Create the outputs of the agent
    igs.output_create("note", igs.INTEGER_T, None)
    igs.output_set_description("note", """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\nhr { height: 1px; border-width: 0; }\nli.unchecked::marker { content: \"\\2610\"; }\nli.checked::marker { content: \"\\2612\"; }\n</style></head><body style=\" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Number of the note found wich correspond of the input of a MIDI keyboard</p></body></html>""")
    igs.output_add_constraint("note", "range [0,127]")
    

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    get_current_note(printOut=True)

    igs.stop()