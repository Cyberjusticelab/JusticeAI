import os
from langdetect import detect
from util.constant import Path


def is_language_type(text, language):
    """
    :param text: language detection will be run on this text
    :param language: desired language to be detected
    :return: returns true if this text is written in the language specified else false
    """
    language_detected = detect(text)
    if language_detected == language:
        return True
    return False


def remove_language_type_from_directory(directory_path, language):
    """
    :param directory_path: directory path to search in
    :param language: language that needs to be removed
    :return: total files removed
    """
    count = 0
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_content = open(directory_path + filename, "r", encoding="ISO-8859-1").read()
            if is_language_type(file_content, language):
                count += 1
                os.remove(Path.raw_data_directory + filename)
    return count


if __file__ == "__main__":
    remove_language_type_from_directory(Path.raw_data_directory, "en")
