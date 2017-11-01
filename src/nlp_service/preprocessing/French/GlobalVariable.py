from nltk.corpus import stopwords


# #################################################
# GLOBAL
# -------------------------------------------------
# Change these variables to make code work on your machine
# tmp solution since we can't download models online via
# HTTP
class Global:
    Precedence_Directory = r"/home/charmander/Data/text_bk/"
    Word_Vector_Directory = r'/home/charmander/Data/french_vectors/wiki.fr.vec.bin'

    # Add stop words as you see fit
    custom_stop_words = stopwords.words('french') + \
                        [',', ';', '.', '!', '?',
                         'c', '(', ')']