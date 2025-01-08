#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  PitchDetector
#  Created by Ingenuity i/o on 2025/01/04
#
# no description


import sys
import ingescape as igs

import aubio
import numpy as np
import pyaudio
import time
import argparse
import queue
import music21  

VOLUME_TRESH = 0.01
SILENCE_TRESH = -32
DEVICE_NUMBER = 7

def get_current_note(volume_thresh=VOLUME_TRESH, printOut=False):

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

            if pitch and volume > volume_thresh:  
                current_pitch.frequency = pitch
            else:
                continue

            if printOut:
                print(current_pitch)
                print(current_pitch.name)
                igs.output_set_string("noteName", current_pitch.nameWithOctave)
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

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_class("PitchDetector")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))


    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    igs.output_create("noteName", igs.STRING_T, None)
    igs.output_create("note", igs.INTEGER_T, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))
    
    #input()

    get_current_note(volume_thresh=VOLUME_TRESH, printOut=True)

    igs.stop()


