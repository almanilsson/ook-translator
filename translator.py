"""
Ook Translator
--------------

Translates text between human language and the Librarian's "ook" language
from Terry Pratchetts Discworld.

Functions:
- combine_characters(): Recursively combines possible combinations of strings in a given list.
- translate_human(): Converts human text to Orangutan.
- translate_orangutan(): Converts Orangutan text to human.
- read_text_file(): Reads and returns the content of a text file.
- write_translated_text_file(): Writes translated text to a new file with "_translated" added.

Constants:
- OOK_TO_HUMAN: Mapping of Ook sound groups to human letter groups.
- HUMAN_TO_OOK: Mapping of human letter groups to Ook sound groups.
"""

import re
import os
from wordfreq import zipf_frequency

OOK_TO_HUMAN = {
    "ok": list("AOU"),
    "ook": list("BP"),
    "okk": list("CSZ"),
    "Ok": list("DT"),
    "oK": list("EIY"),
    "ookk": list("FVW"),
    "OK": list("GKQX"),
    "Ookk": list("H"),
    "oOkk": list("J"),
    "oOKk": list("L"),
    "OokK": list("MN"),
    "oOkK": list("R"),
}
HUMAN_TO_OOK = {
    "AOU": "ok",
    "BP": "ook",
    "CSZ": "okk",
    "DT": "Ok",
    "EIY": "oK",
    "FVW": "ookk",
    "GKQX": "OK",
    "H": "Ookk",
    "J": "oOkk",
    "L": "oOKk",
    "MN": "OokK",
    "R": "oOkK",
}


def combine_characters(char_list):
    """
    Recursively combines possible combinations of strings in a given list
    and returns a new list with said combinations.

    """
    if len(char_list) == 1:
        return char_list[0]
    m = [a + b for a in char_list[0] for b in char_list[1]]
    char_list = [m] + char_list[2:]
    return combine_characters(char_list)


def read_text_file(file_path):
    """
    Reads and returns the content of a text file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_translated_text_file(file_path, content):
    """
    Writes translated text to a new file with "_translated" added.
    """
    base, ext = os.path.splitext(file_path)
    output_path = f"{base}_translated{ext}"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def translate_orangutan(file_path):
    """
    Translate text from Orangutan language to human language.

    Reads a text file written in Orangutan, translates each
    sound group to possible English letters, and writes the result to a new file.
    If multiple possible translations exist, they are shown in brackets.

    """
    # Read input file

    input_text = read_text_file(file_path)

    # Stop if input contains unsupported characters
    if "_" in input_text or "-" in input_text or "'" in input_text:
        raise ValueError("contains unhandled characters")

    # Split text on spaces to extract oook words
    input_words = input_text.split(" ")
    translated_text = ""

    for word in input_words:

        # Split word into sound groups based on where there is a "k" followed by an "o"
        # okok -> ok ok
        ook_syllables = re.split(r"(?i)(?<=k)(?=o)", word)

        # Define list for possible character matches and map ook sound groups to letter options
        char_options = [[] for i in range(len(ook_syllables))]
        for i, syllable in enumerate(ook_syllables):
            for ook_sound, char_group in OOK_TO_HUMAN.items():
                if syllable == ook_sound:
                    char_options[i] = char_group

        # Recursively combine possible letters into word candidates
        character_combinations = combine_characters(char_options)
        possible_word_list = []

        # Keep only words that exist in English (zipf_frequency > 0)
        for combination in character_combinations:
            if zipf_frequency(combination, "en") > 0.0:
                possible_word_list.append(combination)

        # Add result to translated text, comma-separated within <> if several matches exist
        if len(possible_word_list) == 0:
            translated_text += "<no valid words>"
        elif len(possible_word_list) > 1:
            translated_text += "<" + ", ".join(possible_word_list) + ">"
        else:
            translated_text += possible_word_list[0]
        translated_text += " "

    # Write translated output to new file
    write_translated_text_file(file_path, translated_text)


def translate_human(file_path):
    """
    Translate text from human language to Orangutan language.

    Reads an input text file in plain English, replaces each letter with the
    corresponding ook sound group, and writes the translated text to a new file.
    Punctuation and characters without defined mappings are kept unchanged
    (because Orangutans do not use those).
    """

    # Read input file
    input_text = read_text_file(file_path)

    translated_text = ""

    # Replace letters with corresponding Ook sounds
    for char in input_text:
        upper_char = char.upper()
        ook = None
        for char_group, ook_sound in HUMAN_TO_OOK.items():
            if upper_char in char_group:
                ook = ook_sound
                break
        if ook:
            translated_text += ook
        else:
            translated_text += char

    # Write translated output to new file
    write_translated_text_file(file_path, translated_text)
