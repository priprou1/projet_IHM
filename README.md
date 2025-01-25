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

You can also start each of the agents separetly, by following the **README** in each subfolder of the folder agent.

You need also in the Ingescape circle v.4 software and in the Whiteboard agent to choose the network device and the port that you gave before.

## Game interaction

You can start

### The differents parameters

You can change differents parameters of the game inside the PitchBird box in Ingescape circle v.4 :

- **The volume threshold :** In the double writer at the top, linked to the **volumThresh** input of the **PitchDetector** agent, you can put a double between **0.1** and **1**.\
  This parameter is useful to adjust the volume threshold in order to avoid noises and detect corectly the pitch from the microphone.
- **The minimum and maximum notes :** In the first integer writer from the top, linked to the **bmax** input of the **Bird** and **Obstacle** agents you can set the maximum note and respectively the minimum note in the second integer writer from the top linked to the **bmin** input of the same agents, you can put an integer between **0** an **127** (corresponding to MIDI output note). Be careful to set a minimum value lower than the maximum value.\
  This parameter can be useful to adjust the range of the note displayed, because we all have different voice range (for example a bass can reach lower notes than a soprano).
- **The offset :** In the third integer writer from the top, linked to the **offset** input of the **Obstacle** agent, you can put an integer with a minimum of #TODO .\
  This parameter can be useful to #TODO
- **The refresh time :** In the **Timer** at the bottom, linked to the **clock** input of the **Obstacle** agent, you can set the refresh time.

## Credits

- The keyboard agent has been made by another group, they kindly gave it to us in order to interact with it.\
  Thank you Xavier Naxara, Ulysse Radisson and #TODO for this agent.

- The WhiteBoard agent has been made by the ingenuity i/o society. You can find their gitLab repository [there](https://gitlab.ingescape.com/learn/whiteboard).

- All the other agents, the interaction between them, the requirements and the V&Vs scripts has been made by our group composed by Lucas Bolbènes, Armand Claveau and Priscilia Gonthier.
