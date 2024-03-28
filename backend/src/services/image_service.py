import os
from flask import send_file, make_response
from werkzeug.utils import secure_filename
from PIL import Image

class ImageService:
    def __init__(self, storage_folder):
        self.storage_folder = storage_folder
        os.makedirs(storage_folder, exist_ok=True)

    def upload_image(self, request, image_type):
        """
        Generalized image upload function.
        
        :param request: Flask request object.
        :param image_type: A string indicating the type of image ('content' or 'style').
        :return: A success message with the filename or an error message.
        """
        if 'image' not in request.files:
            return 'No image file provided', 400
        
        file = request.files['image']
        # Optionally, validate the image
        # self.validate_image(file)
        
        filename = f"{image_type}_{secure_filename(file.filename)}"  # Example of adding a prefix
        
        self.save_image(file, filename)
        return f'{image_type.capitalize()} image uploaded successfully: {filename}', 200

    def validate_image(self, file):
        # Implement your validation logic here (e.g., file type, size checks)
        pass

    def save_image(self, file, filename):
        # Ensure filename is secure
        filename = secure_filename(filename)
        file_path = os.path.join(self.storage_folder, filename)
        
        # Assuming file is a Flask `FileStorage` object; adjust as necessary
        file.save(file_path)
        return file_path

    def get_image(self, filename):
        file_path = os.path.join(self.storage_folder, secure_filename(filename))
        if not os.path.exists(file_path):
            # File does not exist, return an error message
            error_message = "The requested image does not exist."
            return make_response(error_message, 404)  # 404 Not Found

        try:
            return send_file(file_path, mimetype='image/jpeg')  # Adjust MIME type as necessary
        except Exception as e:
            # Handle unexpected errors
            error_message = f"An error occurred: {str(e)}"
            return make_response(error_message, 500)  # 500 Internal Server Error
