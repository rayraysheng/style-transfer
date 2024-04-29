from flask import Flask
from flask_cors import CORS
from controllers.api_controller import upload_content_image, get_default_styles, generate_style, synthesize_image, download_image

def create_app():
    app = Flask(__name__)
    
    # Load configuration from `config.py`
    app.config.from_pyfile('config.py')

    # Enable CORS for all domains on all routes
    CORS(app)

    # Define routes
    app.add_url_rule('/api/upload/content', view_func=upload_content_image, methods=['POST'])
    app.add_url_rule('/api/default-styles', view_func=get_default_styles, methods=['GET'])
    app.add_url_rule('/api/style-generation', view_func=generate_style, methods=['POST'])
    app.add_url_rule('/api/synthesis', view_func=synthesize_image, methods=['POST'])
    app.add_url_rule('/api/result', view_func=download_image, methods=['GET'])

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
