import os

from werkzeug.utils import secure_filename

from app import app

UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER_TEST = 'uploadsTest'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


def upload_file(file, file_path, filename):
    # Create the directory
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file.save(os.path.join(file_path, filename))


def sanitize_name(file):
    return secure_filename(file.filename)


def generate_path(conversation_id, file_id, testing=False):
    return '{}/conversations/{}/{}'.format((UPLOAD_FOLDER_TEST if testing else UPLOAD_FOLDER), conversation_id, file_id)


def is_accepted_format(file):
    filename = file.filename
    return '.' in filename and \
           get_file_extension(file) in ALLOWED_EXTENSIONS


def get_file_extension(file):
    return file.filename.rsplit('.', 1)[1].lower()


def get_accepted_formats_string():
    return ", ".join(ALLOWED_EXTENSIONS)
