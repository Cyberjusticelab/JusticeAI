import nltk
import urllib
import os
import time
from threading import Thread
from sys import stdout

nltk.download('punkt')
nltk.download('stopwords')


def monitorDownload(filename, filesize):
    time.sleep(2)
    current_size = 0
    limit = filesize * 0.99
    while limit > current_size:
        current_size = os.stat(filename).st_size
        percentage = (current_size / filesize * 1.00) * 100
        percentage = float("{0:.2f}".format(percentage, 2))
        stdout.write("\r%s - Download percentage: %f%%" % (filename, percentage))
        stdout.flush()
        time.sleep(3)
    print("\n[END] Downloading Binary for Word2Vec Model")


# Checks if file exists before downloading
script_dir = os.path.dirname(__file__)
rel_path = r'WordVectors/non-lem.bin'
abs_file_path = os.path.join(script_dir, rel_path)

if not os.path.exists(abs_file_path):
    print("[START] Downloading Binary for Word2Vec Model")
    thr = Thread(target=monitorDownload, args=(abs_file_path, 312726847,))
    thr.start()
    urllib.request.urlretrieve(
        "http://embeddings.org/frWac_non_lem_no_postag_no_phrase_500_skip_cut100.bin", abs_file_path)
else:
    print("Word Vector binary file requirement already satisfied.")
