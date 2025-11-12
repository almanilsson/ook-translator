import os
def identify_language(file_path: str) -> str:
    """
    Identify if the text file is in human or orangutan.
    Checks the first line: if it only contains 'o' and 'k' (case-insensitive),
    it assumes orangutan.

    Parameters
    file_path : str
        Path to the input text file to read. The file must be UTF-8 encoded.

    Returns
    str
        The language identified
    """
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip().lower()

    # If only contains o and k its orangutan, or a stressed human. We hope and assume it is the former
    if all(ch in "ok" for ch in first_line if ch.isalpha()):
        return "orangutan"
    else:
        return "human"

def read_text_file(file_path: str) -> str:
    """
    Reads and returns the content of a text file.

    Parameters
    file_path : str
        Path to the input text file to read. The file must be UTF-8 encoded.

    Returns
    str
        The full text content of the file as a single string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_translated_text_file(output_path: str, content: str) -> None:
    """
    Writes translated text to a new file with "_translated" added.

    Parameters
    file_path : str
        Path to the original input text file. Used to derive the output filename.
    content : str
        Translated text to be written to the new file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)