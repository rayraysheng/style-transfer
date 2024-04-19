from flask import Flask, request, jsonify, send_file
import os
from dotenv import load_dotenv

from services.image_service import save_image, get_image_path, delete_image
from services.style_transfer_service import perform_style_transfer
from services.text_to_image_service import generate_style_image

load_dotenv()

app = Flask(__name__)

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8080')

@app.route('/api/upload/content', methods=['POST'])
def upload_content_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        image_path = save_image(file, 'content')
        return jsonify({"contentImageUrl": image_path}), 201

@app.route('/api/default-styles', methods=['GET'])
def get_default_styles():
    styles = [{"id": i, "url": f"{BASE_URL}/static/images/style/default{i}.png"} for i in range(1, 7)]
    return jsonify({"styles": styles}), 200

@app.route('/api/style-generation', methods=['POST'])
def generate_style():
    caption = request.json.get('caption', '')
    if not caption:
        return jsonify({"error": "Caption is required"}), 400

    output_path = generate_style_image(caption)  # This saves the image and returns the local path
    style_image_url = f"{BASE_URL}/" + output_path.strip(".")

    return jsonify({"styleImageUrl": style_image_url}), 201


@app.route('/api/synthesis', methods=['POST'])
def synthesize_image():
    content_url = request.json.get('contentImageUrl')
    style_url = request.json.get('styleImageUrl')
    if not content_url or not style_url:
        return jsonify({"error": "Both content and style image URLs are required"}), 400
    result_url = perform_style_transfer(content_url, style_url)
    return jsonify({"resultImageUrl": result_url}), 201

@app.route('/api/result', methods=['GET'])
def download_image():
    image_path = request.args.get('image_path')
    if not image_path:
        return jsonify({"error": "Image path is required"}), 400
    return send_file(image_path, as_attachment=True)

@app.route('/api/refresh', methods=['POST'])
def refresh_image():
    caption = request.json.get('caption')
    content_url = request.json.get('contentImageUrl')
    if not caption or not content_url:
        return jsonify({"error": "Caption and content image URL are required"}), 400
    new_style_url = generate_style_image(caption)  # Re-generate style image with the same caption
    new_result_url = perform_style_transfer(content_url, new_style_url)
    return jsonify({"newResultImageUrl": new_result_url}), 201
