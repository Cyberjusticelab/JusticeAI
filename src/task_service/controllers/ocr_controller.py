from flask import jsonify, abort, make_response

from postgresql_db.models import *

# Logging
import logging
import sys

import pytesseract
import cv2

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


def extract_text(conversation_id, image_data):
    # TODO: document controller method
    """
    """
    # TODO: use imdecode to pass image data directly instead of reading from disk
    img = cv2.imread('/usr/src/app/src/task_service/test.png')
    example_text = pytesseract.image_to_string(img, lang='eng')

    return jsonify({
        'image_text': example_text
    })
