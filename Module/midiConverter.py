#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8
#
#  Authors : Lucas Bolbènes, Armand Claveau, Priscilia Gonthier


"""
Module for converting MIDI numbers to musical note strings.

This module provides utilities for working with MIDI numbers, 
including converting them to human-readable note names.

Functions:
    midiToString(midiNumber): Converts a MIDI number to a note string.

Constants:
    NOTE_NAMES: A list of note names in an octave.

Example:
    >>> midiToString(60)
    'C4'
"""

# Constants
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def midiToString(midiNumber):
    """
    Converts a MIDI number to its corresponding musical note string.
    Args:
        midiNumber (int): The MIDI number to convert. Must be between 0 and 127.
    Returns:
        str: The musical note string corresponding to the given MIDI number.
    Raises:
        ValueError: If the MIDI number is not between 0 and 127.
    Example:
        >>> midiToString(60)
        'C4'
    """
    if 0 <= midiNumber <= 127:
        note = NOTE_NAMES[midiNumber % 12]
        octave = midiNumber // 12 - 1
        return f"{note}{octave}"
    else:
        raise ValueError("MIDI number must be between 0 and 127")

# Example usage
if __name__ == "__main__":
    midiNumber = 60
    print(midiToString(midiNumber))  # Output: C4
