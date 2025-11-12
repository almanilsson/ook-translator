from ook_translator.utils import read_text_file, write_translated_text_file
def translate_human(file_path: str, output_path: str) -> None:
    """
    Translate text from human language to Orangutan language.

    Reads an input text file in plain English, replaces each letter with the
    corresponding ook sound group, and writes the translated text to a new file.
    Punctuation and characters without defined mappings are kept unchanged.

    Parameters
    file_path : str
        Path to the input text file containing human text.
    output_path : str
        Path where the translated file will be saved.
    """

    # Mapping of letter groups that basically sound the same (if youre northern/central european at least) to Ook sounds
    translation_mapping = {
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

    # Read input file
    input_text = read_text_file(file_path)

    translated_text = ""

    # Replace letters with corresponding Ook sounds
    for char in input_text:
        upper_char = char.upper()
        ook = None
        for char_group, ook_sound in translation_mapping.items():
            if upper_char in char_group:
                ook = ook_sound
                break
        if ook:
            translated_text += ook
        else:
            translated_text += char

    # Write translated output to new file
    write_translated_text_file(output_path, translated_text)
