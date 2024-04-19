import os
from dotenv import load_dotenv

from werkzeug.utils import secure_filename
from flask import current_app

def save_image(file, category):
    """
    Save an uploaded image to the filesystem, categorizing it into 'content', 'style', or 'result'.
    """
    filename = f"{category}.png"
    directory = os.path.join(current_app.config['UPLOAD_FOLDER'], category)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    file.save(file_path)

    base_url = os.getenv('BASE_URL', 'http://localhost:8080')
    relative_path = os.path.relpath(file_path, start=current_app.root_path)

    return f"{base_url}/{relative_path}"

def get_image_path(filename, category):
    """
    Retrieve the absolute path for a saved image based on its category and filename.
    """
    base_url = os.getenv('BASE_URL', 'http://localhost:8080')
    relative_path = os.path.join(current_app.config['UPLOAD_FOLDER'], category, filename)
    return f"{base_url}/{relative_path}"


def delete_image(file_path):
    """
    Delete an image from the filesystem.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
