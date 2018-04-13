import os
import time
import nltk
from sys import exit
from util.constant import Path
from util.log import Log
import subprocess

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('perluniprops')

ADDRESS_INDEX = 0
FILE_SIZE_INDEX = 1

binary_urls = [
    'https://capstone.cyberjustice.ca/data/bin/classifier_labels.bin',
    'https://capstone.cyberjustice.ca/data/bin/multi_class_svm_model.bin',
    'https://capstone.cyberjustice.ca/data/bin/model_metrics.bin',
    'https://capstone.cyberjustice.ca/data/bin/precedent_vectors.bin',
    'https://capstone.cyberjustice.ca/data/bin/tenant_ordered_to_pay_landlord_regressor.bin',
    'https://capstone.cyberjustice.ca/data/bin/tenant_ordered_to_pay_landlord_scaler.bin',
    'https://capstone.cyberjustice.ca/data/bin/similarity_case_numbers.bin',
    'https://capstone.cyberjustice.ca/data/bin/similarity_model.bin',
    'https://capstone.cyberjustice.ca/data/bin/similarity_scaler.bin'
]

if (not os.environ['CJL_USER']) or (not os.environ['CJL_PASS']):
    Log.write(
        "You must supply the CJL_USER and CJL_PASS environment variables to download binaries from capstone.cyberjustice.ca")
    exit(1)

for binary_url in binary_urls:
    binary_name = binary_url.split('/')[-1]
    abs_file_path = os.path.join(Path.binary_directory, binary_name)

    Log.write(binary_name)
    status = subprocess.call(
        "wget --quiet --recursive --force-directories --show-progress --progress=bar:force --no-cache --user={} --password={} --output-document={} {}".format(
            os.environ['CJL_USER'], os.environ['CJL_PASS'], abs_file_path, binary_url
        ).split(" "))

    if status != 0:
        Log.write("Non-zero status! {}".format(status))
        exit(1)
