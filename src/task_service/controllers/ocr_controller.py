from flask import jsonify, abort, make_response

from postgresql_db.models import *

# Logging
import logging
import sys

import pytesseract
import cv2
import numpy as np

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


def extract_text(conversation_id, image_data):
    # TODO: document controller method
    """
    """
    img = _get_image_from_data(image_data)
    text = _get_string_from_np_img(img)
    return jsonify({
        'image_text': text
    })

def _get_image_from_file(file_path):
    return cv2.imread(file_path)

def _get_image_from_data(data):
    np_data =  np.fromstring(data, np.uint8)
    return cv2.imdecode(np_data, 0) # 0 indicates grayscale

def _get_string_from_np_img(np_img):
    return pytesseract.image_to_string(np_img, lang='eng')

