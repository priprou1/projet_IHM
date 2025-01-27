#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8
#
#  Authors : Lucas Bolbènes, Armand Claveau, Priscilia Gonthier


"""
Module for converting MIDI numbers to musical note strings and vice versa.

This module provides utilities for working with MIDI numbers, 
including converting them to human-readable note names and 
converting note strings back to their corresponding MIDI numbers.

Functions:
    midi_to_string(midiNumber): Converts a MIDI number to a note string.
    string_to_midi(noteString): Converts a musical note string to its corresponding MIDI number.

Constants:
    NOTE_NAMES: A list of note names in an octave.

Examples:
    >>> midi_to_string(60)
    'C4'
    >>> string_to_midi('C4')
    60

Raises:
    ValueError: Raised when input values are out of the MIDI range or invalid.
"""

# Constants
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def midi_to_string(midiNumber):
    """
    Converts a MIDI number to its corresponding musical note string.

    Args:
        midiNumber (int): The MIDI number to convert. Must be between 0 and 127.

    Returns:
        str: The musical note string corresponding to the given MIDI number.

    Raises:
        ValueError: If the MIDI number is not between 0 and 127.

    Example:
        >>> midi_to_string(60)
        'C4'
    """
    if 0 <= midiNumber <= 127:
        note = NOTE_NAMES[midiNumber % 12]
        octave = midiNumber // 12 - 1
        return f"{note}{octave}"
    else:
        raise ValueError("MIDI number must be between 0 and 127")
    
def string_to_midi(noteString):
    """
    Converts a musical note string to its corresponding MIDI number.

    Args:
        noteString (str): The musical note string (e.g., 'C4', 'D#-1').
                          The note must be a valid note and the octave must be an integer.

    Returns:
        int: The MIDI number corresponding to the given note string.

    Raises:
        ValueError: If the note string is invalid or out of range.

    Example:
        >>> string_to_midi('C4')
        60
    """
    try:
        # Extract the note (e.g., 'C', 'D#')
        note = noteString[:-2] if noteString[-2] == '-' else noteString[:-1]
        # Extract the octave (e.g., -1, 4)
        octave = int(noteString[len(note):])
        
        if note not in NOTE_NAMES:
            raise ValueError(f"Invalid note: {note}")
        
        # Calculate the MIDI number
        midiNumber = (octave + 1) * 12 + NOTE_NAMES.index(note)
        
        # Validate MIDI range
        if 0 <= midiNumber <= 127:
            return midiNumber
        else:
            raise ValueError(f"Note out of MIDI range: {noteString}")
    
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid note string: {noteString}. Error: {e}")

# Example usage
if __name__ == "__main__":
    midiNumber = 60
    print("midi_to_string(",midiNumber,") = ", midi_to_string(midiNumber))  # Output: C4
    noteString = "C4"
    print("string_to_midi(",noteString,") = ",string_to_midi(noteString))  # Output: 60
