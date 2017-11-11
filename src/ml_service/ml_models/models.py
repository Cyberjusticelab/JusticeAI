import os
import joblib


def load_facts_from_bin():
    try:
        print("Loading Preprocessed facts... May take a few seconds")
        __script_dir = os.path.abspath(__file__ + r"/../")
        __rel_path = r'processed_facts.bin'
        file_path = os.path.join(__script_dir, __rel_path)
        file = open(file_path, 'rb')
        model = joblib.load(file)
        print("Loading complete")
        return model
    except BaseException:
        print("Download model binary first")


def load_decisions_from_bin():
    try:
        print("Loading Preprocessed decisions... May take a few seconds")
        __script_dir = os.path.abspath(__file__ + r"/../")
        __rel_path = r'processed_decisions.bin'
        file_path = os.path.join(__script_dir, __rel_path)
        file = open(file_path, 'rb')
        model = joblib.load(file)
        print("Loading complete")
        return model
    except BaseException:
        print("Download model binary first")

def load_updated_facts_from_bin():
    try:
        print("Loading Updated processed facts... May take a few seconds")
        __script_dir = os.path.abspath(__file__ + r"/../")
        __rel_path = r'updated_processed_facts.bin'
        file_path = os.path.join(__script_dir, __rel_path)
        file = open(file_path, 'rb')
        model = joblib.load(file)
        print("Loading complete")
        return model
    except BaseException:
        print("Download model binary first")