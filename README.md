## Prerequisites

- Python3 (https://www.python.org/downloads/)
- Ingescape python binding (from pip)
- Ingescape circle v.4 (on the ingescape website)
- aubio module (from pip)
- pyaudio (form pip, if doesn't work for apt : sudo apt install python3-pyaudio)
- music21

## Install dependencies

A requirements.txt is provided. Install dependencies using pip

```bash
pip install -r requirements.txt
```

## Run

To start the whole game, you need to modify the second line of the script **launch_agents.sh** with a network device and a port.
Then launch this script

Example:

```bash
./launch_agents.sh
```

You can also start each of the agents separetly folowing the readme in each subfolder of the folder agent.
