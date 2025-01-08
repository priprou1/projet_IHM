#!/bin/bash

whiteboard_directory="$(dirname "$0")/../agents/Whiteboard"

gnome_terminal_available=false
if command -v gnome-terminal &> /dev/null; then
    gnome_terminal_available=true
fi

if $gnome_terminal_available; then
    gnome-terminal --tab --title="whiteboard" -- bash -c "$whiteboard_directory/Whiteboard.sh; exec bash"
else
    $whiteboard_directory/Whiteboard.sh
fi
