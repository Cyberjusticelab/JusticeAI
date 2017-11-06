from nltk.corpus import stopwords
import os


def get_french_vector_path():
    try:
        __script_dir = os.path.abspath(__file__ + r"/../../")
        __rel_path = r'WordVectors/non-lem.bin'
        return os.path.join(__script_dir, __rel_path)
    except BaseException:
        print("Please download French Vector")


def get_stop_words():
    return stopwords.words('french') + \
        [',', ';', '.', '!', '?', 'c', '(', ')', 'ainsi',
            'alors', 'au', 'aucuns', 'aussi', 'autre', 'avant', 'avec',
            'avoir', 'bon', 'car', 'ce', 'cela', 'ces', 'ceux',
            'chaque', 'ci', 'comme', 'comment', 'dans', 'des', 'du', 'dedans',
            'dehors', 'depuis', 'devrait', 'doit', 'donc', 'dos', 'début',
            'elle', 'elles', 'en', 'encore', 'essai', 'est', 'et', 'eu', 'fait',
            'faites', 'fois', 'font', 'hors', 'ici', 'il', 'ils', 'la', 'le', 'les',
            'leur', 'là', 'ma', 'maintenant', 'mais', 'mes', 'mine', 'moins',
            'mon', 'mot', 'même', 'ni', 'nommés', 'notre', 'nous', 'ou',
            'où', 'par', 'parce', 'pas', 'peut', 'peu', 'plupart', 'pour',
            'pourquoi', 'quand', 'que', 'quel', 'quelle,''quelles', 'quels',
            'qui', 'sa', 'sans', 'ses', 'seulement', 'si', 'sien,''son', 'sont',
            'sous', 'soyez', 'sur', 'ta', 'tandis', 'tellement', 'tels',
            'tes', 'ton', 'tous''tout', 'trop', 'très', 'tu', 'voient',
            'vont', 'votre', 'vous', 'vu', 'ça', 'étaient', 'état', 'étions', 'été', 'être',
         ]


def get_french_ner_path():
    try:
        __script_dir = os.path.abspath(__file__ + r"/../../")
        __rel_path = r'MLModels/ner_model.pickle'
        return os.path.join(__script_dir, __rel_path)
    except BaseException:
        print("Couldn't find model")

# #################################################
# GLOBAL
# -------------------------------------------------
# Change these variables to make code work on your machine
# tmp solution since we can't download models online via
# HTTP


class Global:
    Precedence_Directory = r"/home/charmander/Data/text_bk/"
    French_Word_Vector_Directory = get_french_vector_path()
    French_NER = get_french_ner_path()
    Word_Vector_Size = 500
    custom_stop_words = get_stop_words()
