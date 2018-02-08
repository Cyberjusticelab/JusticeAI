from flask import jsonify, abort, make_response
import base64

# Logging
import logging
import sys

import pytesseract
import cv2
import numpy as np

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

SUPPORTED_IMAGE_DATA_FORMATS = [
    b'data:image/png;base64,'
]

def extract_text(image_data):
    # TODO: document controller method
    """
    """
    img = _get_image_from_data(image_data)
    if img.any():
        text = _get_string_from_np_img(img)
        return jsonify({
            'image_text': text
        })
    return abort(make_response(jsonify(message='Image data must be in a supported format: {}'.format(SUPPORTED_IMAGE_DATA_FORMATS)), 422))

def _get_image_from_file(file_path):
    return cv2.imread(file_path)

def _get_image_from_data(data):
    '''
    Although the method is meant to operate on base64-encoded png image data as bytes, it will attempt to convert the data given to it to this format.

    Currently, the only supported image data type is 'data:image/png,base64,'

    '''
    if isinstance(data, str):
        data = data.encode('utf-8')
    if data.startswith(b'data:'):
        for supported_format in SUPPORTED_IMAGE_DATA_FORMATS:
            if data.startswith(supported_format):
                data = data[len(supported_format):]
                break
        if data.startswith(b'data:'):
            return None

    data = base64.b64decode(data)
    np_data = np.fromstring(data, np.uint8)
    return cv2.imdecode(np_data, 0) # 0 indicates grayscale

def _get_string_from_np_img(np_img):
    return pytesseract.image_to_string(np_img, lang='eng')

