## Prerequisites

- Python3 (https://www.python.org/downloads/)
- Ingescape python binding (from pip)
- aubio module (from pip)
- pyaudio (form pip, if pip doesn't work : from apt : sudo apt install python3-pyaudio)
- music21 (from pip)

## Install dependencies

A requirements.txt is provided. Install dependencies using pip

```bash
pip install -r requirements.txt
```

## Run

To start the agent, you need to pass an agent name, a network device and a port **in that order** to the main script.
Example:

```bash
python3 main.py MyAgent en0 1337
```
