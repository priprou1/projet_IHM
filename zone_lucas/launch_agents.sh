#!/bin/bash

# Répertoire des agents
sandbox_directory="$HOME/Documents/Ingescape/sandbox/"

# Vérifier les arguments fournis
if [[ $# -lt 3 ]]; then
    echo "Usage: $0 <network_device> <port> <agents...>"
    echo "Exemple: $0 wlp2s0 5760 Bird PitchDetector"
    exit 1
fi

# Récupérer les arguments
network_device="$1"      # Premier argument : interface réseau
port="$2"                # Deuxième argument : port
requested_agents=("${@:3}")   # Récupérer tous les autres arguments comme une liste d'agents

# Lancer chaque agent dans un nouvel onglet
for agent_name in "${requested_agents[@]}"; do
    script_path="$sandbox_directory/$agent_name/main.py"
    if [[ -f "$script_path" ]]; then
        gnome-terminal --tab --title="$agent_name" -- bash -c "python3 $script_path $agent_name $network_device $port; exec bash"
        echo "Agent $agent_name lancé avec $network_device sur le port $port."
    else
        echo "Erreur : L'agent $agent_name est introuvable ou invalide."
    fi
done

echo "Tous les agents demandés et le Whiteboard ont été lancés."

