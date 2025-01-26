## Prerequisites

- Python3 (https://www.python.org/downloads/)
- Ingescape python binding (from pip)
- Ingescape circle v.4 (on the [ingescape website](https://ingescape.com/get/))
- aubio module (from pip)
- pyaudio (form pip, if pip doesn't work : from apt : sudo apt install python3-pyaudio)
- music21 (from pip)

## Install dependencies

A requirements.txt is provided. Install dependencies using pip

```bash
pip install -r requirements.txt
```

## Run

To run the whole game, you need to open the file pitchbird.igssystem in the Ingescape circle v.4 software and connect the network device and the port.\
Modify the second line of the script **launch_agents.sh** with the network device and the port.\
Then start the whiteboard, by launching the script **scripts/launch_whiteboard.sh**. Then connect the whiteboard to the network device and the port that you gave before.\
After you need to launch the script **launch_agents.sh**.

Example:

```bash
./scripts/launch_whiteboard.sh
./launch_agents.sh
```

You can also start each of the agents separetly, by following the **README** in each subfolder of the folder agent.\
You can now start the game.

## Game interaction

To **start** (respectively **stop**) the game you need to click on the impulsion writer linked to the **start** (respectively **stop**) input of the PitchBird box in Ingescape circle v.4.\
To **switch** between the microphone and keyboard input you need to click on the corresponding writer.

### The differents parameters

You can change differents parameters of the game inside the PitchBird box in Ingescape circle v.4 :

- **The volume threshold :** In the double writer at the top, linked to the **volumThresh** input of the **PitchDetector** agent, you can put a double between **0.1** and **1**.\
  This parameter is useful to adjust the volume threshold in order to avoid noises and detect corectly the pitch from the microphone.
- **The minimum and maximum notes :** In the first integer writer from the top, linked to the **bmax** input of the **Bird** and **Obstacle** agents you can set the maximum note and respectively the minimum note in the second integer writer from the top linked to the **bmin** input of the same agents, you can put an integer between **0** an **127** (corresponding to MIDI output note). Be careful to set a minimum value lower than the maximum value.\
  This parameter can be useful to adjust the range of the note displayed, because we all have different voice range (for example a bass can reach lower notes than a soprano).
- **The offset :** In the third integer writer from the top, linked to the **offset** input of the **Obstacle** agent, you can put an integer with a minimum of 10.\
  This parameter can be useful to change the size of the obstacle mouvement.
- **The refresh time :** In the **Timer** at the bottom, linked to the **clock** input of the **Obstacle** agent, you can set the refresh time.

## Credits

- The WhiteBoard agent has been made by the ingenuity i/o society. You can find their gitLab repository [there](https://gitlab.ingescape.com/learn/whiteboard).

- All the other agents, the interaction between them, the requirements, the V&Vs scripts and the midiConverter module has been made by our group composed by Lucas Bolbènes, Armand Claveau and Priscilia Gonthier.
