#!/bin/bash

agents_directory="$(dirname "$0")/../agents"

if [[ $# -lt 3 ]]; then
    echo "Usage: $0 <network_device> <port> <agents...>"
    echo "Exemple: $0 wlp2s0 5670 Bird PitchDetector"
    exit 1
fi

network_device="$1"      
port="$2"               
requested_agents=("${@:3}")   

gnome_terminal_available=false
if command -v gnome-terminal &> /dev/null; then
    gnome_terminal_available=true
fi

for agent_name in "${requested_agents[@]}"; do
    script_path="$agents_directory/$agent_name/main.py"
    if [[ -f "$script_path" ]]; then
        if $gnome_terminal_available; then
            gnome-terminal --tab --title="$agent_name" -- bash -c "python3 $script_path $agent_name $network_device $port; exec bash"
        else
            python3 $script_path $agent_name $network_device $port &
        fi
        echo "Agent $agent_name lancé avec $network_device sur le port $port."
    else
        echo "Erreur : L'agent $agent_name est introuvable ou invalide."
    fi
done
