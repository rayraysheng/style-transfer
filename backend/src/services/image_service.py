import os
from dotenv import load_dotenv
from PIL import Image
import numpy as np

from werkzeug.utils import secure_filename
from flask import current_app

def save_image(file, category):
    """
    Save an uploaded image to the filesystem, categorizing it into 'content', 'style', or 'result'.
    Overwrites any existing file at the destination path.
    """
    filename = f"{category}.png"
    directory = os.path.join(current_app.config['UPLOAD_FOLDER'], category)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    
    # Check if file already exists and log if it does
    if os.path.exists(file_path):
        current_app.logger.info(f"Overwriting existing file: {file_path}")
    
    # Save (and potentially overwrite) the file
    file.save(file_path)

    base_url = os.getenv('BASE_URL', 'http://localhost:8080/')
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

def tensor_to_image(tensor):
    """
    Converts a TensorFlow tensor to a PIL Image.
    """
    if isinstance(tensor, np.ndarray):
        # Assume the tensor data is already in the correct format
        image = Image.fromarray((tensor * 255).astype(np.uint8))
    else:
        raise ValueError("Input needs to be a numpy array.")
    return image

def save_stylized_image_url(tensor, filename='result_image.png'):
    """
    Saves a stylized image tensor to the filesystem under the /src/static/images/result directory
    and returns the URL to this image.
    """
    directory = os.path.join(current_app.root_path, 'src', 'static', 'images', 'result')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, filename)
    image = tensor_to_image(tensor)
    image.save(file_path, 'PNG')

    base_url = os.getenv('BASE_URL', 'http://localhost:8080')
    static_path = os.path.relpath(file_path, start=current_app.root_path)
    
    return f"{base_url}/{static_path.replace(os.sep, '/')}"
