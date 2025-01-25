## Prerequisites

- Python3 (https://www.python.org/downloads/)
- Ingescape python binding (from pip)
- Ingescape circle v.4 (on the ingescape website)
- aubio module (from pip)
- pyaudio (form pip, if pip doesn't work : from apt : sudo apt install python3-pyaudio)
- music21 (from pip)

## Install dependencies

A requirements.txt is provided. Install dependencies using pip

```bash
pip install -r requirements.txt
```

## Run

To start the whole game, you need to open the file pitchbird.igssystem in the Ingescape circle v.4 software. Then modify the second line of the script **launch_agents.sh** with a network device and a port.
Then launch this script

Example:

```bash
./launch_agents.sh
```

You can also start each of the agents separetly, by folowing the readme in each subfolder of the folder agent.

You need also in the Ingescape circle v.4 software and in the Whiteboard agent to choose the network device and the port that you gave before.

## Game interaction

Click

### The differents parameters

You can change differents parameters of the game inside the box PitchBird in Ingescape circle v.4 :

- The volume threshold : In the double writer at the top linked to the **volumThresh** input of the agent **PitchDetector**, you can put a double between **0.1** and **1**. This parameter

## Credits

The keyboard agent has been made by another group, they kindly gave it to us in order to interact with it.\
Thank you Xavier
