"""
Checks that translation produces the expected results.
"""
import os
from src.ook_translator import translate_human


def test_translate_human():
    """
    Translate a known input and check the output content.
    """
    input_file = "test_example.txt"
    output_file = "test_example_translated.txt"
    expected_output = "okokkokkokokkoKokOokKokoOKk" 

    # Create test input file
    with open(input_file, "w", encoding="utf-8") as f:
        f.write("occasional")

    # translate the file
    translate_human.translate_human(input_file,output_file)

    # Check if the output file exists
    assert os.path.exists(output_file)

    #a Assert that content is correct
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == expected_output

    # Clean up test files
    os.remove(input_file)
    os.remove(output_file)

