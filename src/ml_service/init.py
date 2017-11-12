import nltk
import os
import time
import requests
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
        stdout.write("\r%s - Download percentage: %.2f%%" %
                     (filename, percentage))
        stdout.flush()
        time.sleep(3)
    print("\n[END] Downloading Binary for Word2Vec Model")


# Checks if file exists before downloading
script_dir = os.path.dirname(__file__)
rel_path = r'WordVectors/non-lem.bin'
abs_file_path = os.path.join(script_dir, rel_path)

if not os.path.exists(abs_file_path):
    print("[START] Downloading Binary for Word2Vec Model")
    thr = Thread(target=monitorDownload, args=(abs_file_path, 126052447,))
    thr.start()

    response = requests.get('https://capstone.cyberjustice.ca/data/frWac_non_lem_no_postag_no_phrase_200_skip_cut100.bin',
                            auth=(
                                os.environ['CJL_USER'],
                                os.environ['CJL_PASS']),
                            stream=True,
                            verify=False)
    with open(abs_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
else:
    print("Word Vector binary file requirement already satisfied.")
