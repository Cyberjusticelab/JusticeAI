import requests

TASK_URL = "http://task_service:3004"


def ocr_extract_text(file_storage):
    files = {
        'file': (file_storage.filename, file_storage.stream, file_storage.mimetype)
    }
    res = requests.post("{}/{}".format(TASK_URL, "ocr/extract_text"), files=files)
    return res.json()
