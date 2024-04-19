import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Function to load an image and convert it to a tensor
def load_img(path_to_img):
    img = tf.io.read_file(path_to_img)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]  # Add batch dimension
    return img

# Function to preprocess the image
def preprocess_image(image, target_dim):
    # Resize the image so that the shortest dimension becomes target_dim
    shape = tf.cast(tf.shape(image)[1:-1], tf.float32)
    short_dim = min(shape)
    scale = target_dim / short_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    image = tf.image.resize(image, new_shape)

    # Central crop the image
    image = tf.image.resize_with_crop_or_pad(image, target_dim, target_dim)
    return image

# Function to run style prediction
def run_style_predict(preprocessed_style_image, style_predict_model_path):
    interpreter = tf.lite.Interpreter(model_path=style_predict_model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], preprocessed_style_image)
    interpreter.invoke()
    style_bottleneck = interpreter.get_tensor(output_details[0]['index'])
    return style_bottleneck

# Function to perform style transfer
def run_style_transform(style_bottleneck, preprocessed_content_image, style_transform_model_path):
    interpreter = tf.lite.Interpreter(model_path=style_transform_model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], preprocessed_content_image)
    interpreter.set_tensor(input_details[1]['index'], style_bottleneck)
    interpreter.invoke()
    stylized_image = interpreter.get_tensor(output_details[0]['index'])
    return stylized_image

# Main function to perform style transfer from paths
def perform_style_transfer(content_image_path, style_image_path, style_predict_path, style_transform_path):
    # Load images
    content_image = load_img(content_image_path)
    style_image = load_img(style_image_path)

    # Preprocess images
    preprocessed_content_image = preprocess_image(content_image, 384)
    preprocessed_style_image = preprocess_image(style_image, 256)

    # Style prediction
    style_bottleneck = run_style_predict(preprocessed_style_image, style_predict_path)

    # Style transformation
    stylized_image = run_style_transform(style_bottleneck, preprocessed_content_image, style_transform_path)

    # Convert tensor to image and save
    stylized_image = tf.squeeze(stylized_image, axis=0)  # Remove batch dimension
    stylized_image = Image.fromarray((stylized_image.numpy() * 255).astype(np.uint8))
    output_path = content_image_path.replace('/content/', '/result/')
    stylized_image.save(output_path)
    return output_path
