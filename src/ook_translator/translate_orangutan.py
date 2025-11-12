import re
from typing import Union

from wordfreq import zipf_frequency
from ook_translator.utils import read_text_file, write_translated_text_file

def translate_orangutan(file_path: str, output_path: str) -> None:
    """
    Translate text from Orangutan language to human language.

    Reads a text file written in Orangutan, translates each
    sound group to possible English letters, and writes the result to a new file.
    If multiple possible translations exist, they are shown in brackets.

    Parameters
    file_path : str
        Path to the input text file containing Orangutan text.
    output_path : str
        Path where the translated file will be saved.
    """
     # Read input file
    input_text = read_text_file(file_path)
    # Stop if input contains unsupported characters

    if re.search(r"[_\-']", input_text):
        raise ValueError("OokKok?! I don't like that! No joining symbols like _ - or ' allowed >:")

    # Split text on spaces to extract oook words
    # Orangutans do not use punctuation, at least not yet
    input_words = re.sub(r'[^A-Za-z\s]', '', input_text).split()
    translated_text = ""

    frustration_level = 0
    for word in input_words:
        possible_words = produce_possible_words(word)
        actual_words = identify_word(possible_words)
        if not identify_word:
            actual_words = "<no valid words found>"
            frustration_level += 1
            if frustration_level > 3:
                raise ValueError("Are you misspelling things? OkokOokKOk okOokKOKoKoOkK OokKoK!! >:") 
        translated_text += actual_words + " " # add space, also to last word :/
    

    write_translated_text_file(output_path, translated_text)
    return

def produce_possible_words(word: str) -> list[str]:
    """
    Generate all possible human word combinations from a given orangutan (ook) word.

    Parameters
    ook_word : str
        Word in orangutan.

    Returns
    list of str, or str
        All possible human word candidates based on mapping rules.
    """

    translation_mapping = {
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
    # Split word into sound groups based on where there is a "k" followed by an "o"
    # okok -> ok ok
    ook_syllables = re.split(r'(?i)(?<=k)(?=o)', word)
    
    # Define list for possible character matches
    potential_char = [[] for i in range(len(ook_syllables))]

    # Match the syllable to the mapping and retrieve the translated group
    for i, syllable in enumerate(ook_syllables):
        for ook_sound, char_group in translation_mapping.items():
            if syllable == ook_sound:
                potential_char[i] = char_group
    
    # Generate all possible cobinations of the characters 
    return combine_characters(potential_char) # [[A, B],[C]] -> [AC, BC]
                

def combine_characters(char_list: list[list[str]]) -> list[str]:
    """
    Recursively combines possible combinations of strings in a given list
    and returns a new list with said combinations.

    Parameters
    char_list : list
        A list where each element is a list of possible characters or letter groups.

    Returns
    list or str
        A list of all possible string combinations formed by combining the inner lists. Or str if there is only one.
e string
    """
    if len(char_list) == 1:
        return char_list[0]
    # Create all possible combinations of element 0 and 1 in a new list
    combined_char_list = [a + b for a in char_list[0] for b in char_list[1]]
    # Add the ones not yet combined to the new list
    combined_char_list = [combined_char_list] + char_list[2:]   
    # Create all possible combinations of the next two elements recursively
    return combine_characters(combined_char_list)

def identify_word(possible_words: list[str]) -> str:
    """
    Identify which of the possible human words are valid English words.

    Parameters
    possible_words : list
        List of generated human word candidates.

    Returns
    str
        Word or words (given as <word1, word2>) that are valid English words according to the dictionary.
    """

    #match the generated words to those in a frequency based "dictionary"
    actual = [w for w in possible_words if zipf_frequency(w, "en") > 0.0]

    if not actual:
        return "<no valid words found>"
    if len(actual) > 1:
        return f"<{', '.join(actual)}>"
    return actual[0]

