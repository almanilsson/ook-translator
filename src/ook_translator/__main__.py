import argparse
import os

from ook_translator.translate_human import translate_human
from ook_translator.translate_orangutan import translate_orangutan
from ook_translator.utils import identify_language


def main():
    """
    Run Ook Translator from the command line.
    Example:
        python -m ook_translator data/example_message.txt --language human
    """
    parser = argparse.ArgumentParser(
        description="Translate text between human and orangutan."
    )
    parser.add_argument("file", help="Path to the input text file.")
    parser.add_argument(
        "--language",
        choices=["human", "orangutan"],
        help="Specify input language. If not given, it will be autodetected.",
    )

    args = parser.parse_args()
    file_path = args.file
    language = args.language
    base, ext = os.path.splitext(file_path)
    output_path = f"{base}_translated{ext}"

    # Detect language if not provided
    if not language:
        language = identify_language(file_path)
        print(f"Detected language: {language}")

    if language == "human":
        print("Translating human to orangutan...")
        translate_human(file_path, output_path)

    elif language == "orangutan":
        print("Translating orangutan to human...")
        translate_orangutan(file_path, output_path)
    
    print(f"Translation done! Saved as {output_path}")


if __name__ == "__main__":
    main()
