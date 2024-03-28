from flask import Flask
from api_controller import api_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register the API blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 8080)
