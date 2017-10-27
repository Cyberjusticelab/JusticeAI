import flask
from flask import jsonify
from glob import glob
import os
import re
import json

def get_legal_documents():
    filepaths = glob(os.getcwd() + '/legal/*.json')
    filenames = [filepath.split('/').pop() for filepath in filepaths]

    # Find all document types and their highest version numbers
    highest_document_version = {}
    for filename in filenames:
        match = re.search('(.+)-v(\d+)\.json', filename)
        if match:
            document_type = match.group(1)
            version_number = int(match.group(2))
            if document_type in highest_document_version:
                if version_number > highest_document_version[document_type]:
                    highest_document_version[document_type] = version_number
            else:
                highest_document_version[document_type] = version_number

    # Read documents as JSON for highest versions
    document_list = []
    for document, version in highest_document_version.items():
        document_path = os.getcwd() + '/legal/{}-v{}.json'.format(document, version)
        with open(document_path, 'r') as f:
            document_dict = json.load(f)
        document_list.append(document_dict)

    return jsonify(document_list)
