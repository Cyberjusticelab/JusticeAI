from flask import jsonify, abort, make_response

from postgresql_db.models import *

from task_service.app import db

# Logging
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


def extract_text(conversation_id, image_data):
    # TODO: document controller method
    """
    """
    return jsonify({
        'image_text': image_data
    })

if __name__ == '__main__':
    extract_text(1, 'this is image data')
