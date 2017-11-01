
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
        stdout.write("\r%s - Download percentage: %f%%" % (filename, percentage))
        stdout.flush()
        time.sleep(3)


print("[START] Downloading Binary for Word2Vec Model")
thr = Thread(target=monitorDownload, args=('non-lem.bin', 312726847,))
thr.start()
urllib.request.urlretrieve(
    "http://embeddings.org/frWac_non_lem_no_postag_no_phrase_500_skip_cut100.bin", "non-lem.bin")
print("[END] Downloading Binary for Word2Vec Model")
