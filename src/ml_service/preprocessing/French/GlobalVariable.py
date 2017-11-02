from nltk.corpus import stopwords
import os


def get_path():
    try:
        __script_dir = os.path.abspath(__file__ + r"/../../../")
        __rel_path = r'WordVectors/non-lem.bin'
        return os.path.join(__script_dir, __rel_path)
    except:
        return ""


# #################################################
# GLOBAL
# -------------------------------------------------
# Change these variables to make code work on your machine
# tmp solution since we can't download models online via
# HTTP
class Global:
    Precedence_Directory = r"/home/charmander/Data/text_bk/"
    Word_Vector_Directory = get_path()

    # Add stop words as you see fit
    custom_stop_words = stopwords.words('french') + \
                        [',', ';', '.', '!', '?', 'c', '(', ')', 'ainsi']
