import re
import os
from wordfreq import zipf_frequency

def translate_orangutang(file_path):
    input_file = open(file_path, "r", encoding="utf-8")
    input_text = input_file.read()
    input_file.close()

    if "_" in input_text or "-" in input_text or "'" in input_text:
        raise ValueError("contains unhandled characters")
    
    input_words = input_text.split(" ")
    translated_text = ""

    for word in input_words:
        translation_map = {
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

        ook_syllables = re.split(r"(?i)(?<=k)(?=o)", word)
        char_options = [[] for i in range(len(ook_syllables))]

        for i in range(len(ook_syllables)):
            for ook_sound, char_group in translation_map.items():
                if ook_syllables[i] == ook_sound:
                    char_options[i] = char_group

        def combine_characters(char_list):
            if len(char_list) == 1:
                return char_list[0]
            m = [a + b for a in char_list[0] for b in char_list[1]]
            char_list = [m] + char_list[2:]
            return combine_characters(char_list)
        character_combinations = combine_characters(char_options)
        possible_word_list = []

        for combination in character_combinations:
            if zipf_frequency(combination, "en") > 0.0:
                possible_word_list.append(combination)

        if len(possible_word_list) == 0:
            translated_text += "<no valid words>"
        elif len(possible_word_list) > 1:
            translated_text += "<" + ", ".join(possible_word_list) + ">"
        else:
            translated_text += possible_word_list[0]
        translated_text += " "
    
    base, ext = os.path.splitext(file_path)
    output_path = f"{base}_translated{ext}"
    output_file = open(output_path, "w", encoding="utf-8")    
    output_file.write(translated_text)
    output_file.close()

def translate_human(file_path):
    input_file = open(file_path, "r", encoding="utf-8")
    input_text = input_file.read()
    input_file.close()

    translation_map = {
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

    translated_text = ""
    for char in input_text:
        upper_char = char.upper()
        ook = None
        for char_group, ook_sound in translation_map.items():
            if upper_char in char_group:
                ook = ook_sound
                break
        if ook:
            translated_text += ook
        else:
            translated_text += char

    base, ext = os.path.splitext(file_path)
    output_path = f"{base}_translated{ext}"
    output_file = open(output_path, "w", encoding="utf-8")
    output_file.write(translated_text)
    output_file.close()


# translate_orangutan("ok.txt")
translate_human("example.txt")