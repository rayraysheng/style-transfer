import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask settings
DEBUG = True 
PORT = 8080   # The port to listen on
HOST = '0.0.0.0'  # Host to listen on. '0.0.0.0' makes the server available network-wide

# Path settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# OpenAI API settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
