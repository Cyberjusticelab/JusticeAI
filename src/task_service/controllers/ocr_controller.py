from flask import jsonify, abort, make_response
import base64

import pytesseract
import cv2
import numpy as np
import io

# This is the height of the image used to align the document
# A lower value is faster to compute but less accurate than a higher value
ALIGNMENT_RESIZE_HEIGHT = 500

# The area of the document we are trying to align cannot be less than 1/4 of the entire image area
ALIGNMENT_PERCENT_AREA_DOCUMENT_MUST_COVER = 0.25


def extract_text(file_storage):
    # TODO: document controller method
    """
    """
    img = _get_image_from_file_storage(file_storage)
    img = _align_document_from_img(img)
    if img.any():
        text = _get_string_from_np_img(img)
        return jsonify({
            'image_text': text
        })
    return abort(make_response(
        jsonify(message='Image data must be in a supported format: {}'.format(SUPPORTED_IMAGE_DATA_FORMATS)), 422))


def _get_image_from_file(file_path):
    return cv2.imread(file_path, 0)  # 0 indicates grayscale


def _get_image_from_file_storage(file_storage):
    '''
    Please refer to backend_service's conversation_controller.upload_file for supported image formats.
    '''
    in_memory_file = io.BytesIO()
    file_storage.save(in_memory_file)
    np_data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    return cv2.imdecode(np_data, 0)  # 0 indicates grayscale


def _get_string_from_np_img(np_img):
    return pytesseract.image_to_string(np_img, lang='eng')


def _resize(img, height):
    ratio = height / img.shape[0]
    return cv2.resize(img, (int(ratio * img.shape[1]), height))


def _filter_blur(img):
    img = cv2.bilateralFilter(img, 5, 250, 250)  # reduces noise but preserves edges
    return cv2.GaussianBlur(img, (5, 5), 0)  # blurs entire image


def _binarize(img):
    """
    Uses Otsu' adaptive thresholding to convert the image to black/white pixels based on its immediate surroundings
    """
    img = _filter_blur(img)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img


def _compute_all_edges(img):
    return cv2.Canny(img, 200, 250)


def _compute_all_contours(img):
    _, contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def _get_img_dimensions(img):
    # Be sure to only call this on a filtered & binarized image
    return _compute_all_edges(img).shape


def _get_corner_array(height=0, width=0):
    return np.array([
        [0, 0],
        [0, height],
        [width, height],
        [width, 0]
    ], np.float32)


def _sort_corners(pts):
    """
    Sort corners: top-left, bot-left, bot-right, top-right
    """
    diff = np.diff(pts, axis=1)
    summ = pts.sum(axis=1)
    return np.array([
        pts[np.argmin(summ)],
        pts[np.argmax(diff)],
        pts[np.argmax(summ)],
        pts[np.argmin(diff)]
    ], np.float32)


def _find_document_corners(resized_img):
    contours = _compute_all_contours(resized_img)
    resized_height, resized_width = _get_img_dimensions(resized_img)
    full_resized_image_area = resized_height * resized_width

    # Default to the smallest possible document area and save any larger document areas
    largest_document_area = full_resized_image_area * ALIGNMENT_PERCENT_AREA_DOCUMENT_MUST_COVER

    # Default to largest: no modification to the image if no document is found
    largest_document_corners = _get_corner_array(resized_height, resized_width)

    for contour in contours:
        contour_perimeter = cv2.arcLength(contour, True)
        approximate_polygonal_contour = cv2.approxPolyDP(contour, 0.03 * contour_perimeter, True)

        # All pages have 4 corners and are convex
        if (len(approximate_polygonal_contour) == 4 and
                cv2.isContourConvex(approximate_polygonal_contour) and
                cv2.contourArea(approximate_polygonal_contour) > largest_document_area):
            largest_document_area = cv2.contourArea(approximate_polygonal_contour)
            largest_document_corners = approximate_polygonal_contour

    return largest_document_corners


def _get_transformed_dimensions_of_tilted_document(corners):
    """
    Using Euclidean distance, calculate the height and width of the final rendered image
    """
    corners = _sort_corners(corners[:, 0])
    height = max(
        np.linalg.norm(corners[0] - corners[1]),
        np.linalg.norm(corners[2] - corners[3])
    )
    width = max(
        np.linalg.norm(corners[1] - corners[2]),
        np.linalg.norm(corners[3] - corners[0])
    )
    return (height, width)


def _align_document_from_img(img):
    original_height, original_width = _get_img_dimensions(img)
    resized_img = _resize(img, ALIGNMENT_RESIZE_HEIGHT)
    resized_img = _binarize(resized_img)

    initial_corners = _find_document_corners(resized_img)

    # Scale the corners found on the resized image to the original image
    initial_corners = initial_corners.dot(original_height / ALIGNMENT_RESIZE_HEIGHT).astype(np.float32)

    final_height, final_width = _get_transformed_dimensions_of_tilted_document(initial_corners)
    final_corners = _get_corner_array(height=final_height, width=final_width)
    M = cv2.getPerspectiveTransform(initial_corners, final_corners)
    return cv2.warpPerspective(img, M, (int(final_width), int(final_height)))


if __name__ == '__main__':
    original_img = _get_image_from_file(
        '/home/lancelafontaine/repos/JusticeAI/src/task_service/test/ocr/images/lease_tilted.jpg')
    new_image = _align_document_from_img(original_img)
    cv2.imwrite("output.png", new_image)
