from task_service.controllers import ocr_controller
import numpy as np
from urllib.request import urlopen

TEXT_FROM_IMAGE_FILE = "Competitive Programmer’s Handbook\n\nAntti Laaksonen\n\nDraft December 10, 2017"

def test_get_image_from_file():
    img = ocr_controller._get_image_from_file('/usr/src/app/src/task_service/test/ocr/images/test.png')
    assert isinstance(img,(np.ndarray, np.generic))

def test_get_image_from_data():
    img_data = urlopen('file:///usr/src/app/src/task_service/test/ocr/images/test.png').read()
    img = ocr_controller._get_image_from_data(img_data)
    assert isinstance(img,(np.ndarray, np.generic))

def test_get_string_from_file_np_img_data():
    img = ocr_controller._get_image_from_file('/usr/src/app/src/task_service/test/ocr/images/test.png')
    text = ocr_controller._get_string_from_np_img(img)
    assert text == TEXT_FROM_IMAGE_FILE

def test_get_string_from_file_np_img_data():
    img_data = urlopen('file:///usr/src/app/src/task_service/test/ocr/images/test.png').read()
    img = ocr_controller._get_image_from_data(img_data)
    text = ocr_controller._get_string_from_np_img(img)
    assert text == TEXT_FROM_IMAGE_FILE







