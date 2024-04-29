import os
from dotenv import load_dotenv
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import requests
from PIL import Image
from io import BytesIO

# Load environment variables from .env
load_dotenv()

# Set up Matplotlib configurations
mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False

# Retrieve environment variables with fallbacks
base_url = os.getenv('BASE_URL', 'http://localhost:8080/')
img_path = os.getenv('IMG_PATH', 'static/images/')
models_path = os.getenv('MODELS_PATH', 'static/models/')
style_predict_fn = os.getenv('STYLE_PREDICT_FN', 'predict.tflite')
style_transform_fn = os.getenv('STYLE_TRANSFORM_FN', 'transfer.tflite')
stylized_fn = os.getenv('STYLIZED_FN', 'stylized.png')
blended_fn = os.getenv('BLENDED_FN', 'blended.png')

# Construct full paths
style_predict_path = os.path.join(models_path, style_predict_fn)
style_transform_path = os.path.join(models_path, style_transform_fn)

stylized_image_path = os.path.join(img_path, 'result', stylized_fn)
blended_image_path = os.path.join(img_path, 'result', blended_fn)

# Function to load an image from a file, and add a batch dimension.
def load_img(path_to_img):
    """Load an image from a file or URL, and add a batch dimension."""
    if path_to_img.startswith('http'):
        # The path is a URL
        response = requests.get(path_to_img)
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if not already (important for consistency across different image formats)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img = np.array(img)
        img = tf.convert_to_tensor(img, dtype=tf.float32)
    else:
        # The path is a local file
        img = tf.io.read_file(path_to_img)
        img = tf.io.decode_image(img, channels=3, expand_animations=False)
    
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]  
    img = (img - tf.reduce_min(img)) / (tf.reduce_max(img) - tf.reduce_min(img))

    return img

# Function to pre-process by resizing an central cropping it.
def preprocess_image(image, target_dim):
  # Resize the image so that the shorter dimension becomes 256px.
  shape = tf.cast(tf.shape(image)[1:-1], tf.float32)
  short_dim = min(shape)
  scale = target_dim / short_dim
  new_shape = tf.cast(shape * scale, tf.int32)
  image = tf.image.resize(image, new_shape)

  # Central crop the image.
  image = tf.image.resize_with_crop_or_pad(image, target_dim, target_dim)

  return image

# Function to display an image.
def imshow(image, title=None):
  if len(image.shape) > 3:
    image = tf.squeeze(image, axis=0)

  plt.imshow(image)
  if title:
    plt.title(title)

# Function to run style prediction on preprocessed style image.
def run_style_predict(preprocessed_style_image):
  # Load the model.
  interpreter = tf.lite.Interpreter(model_path=style_predict_path)

  # Set model input.
  interpreter.allocate_tensors()
  input_details = interpreter.get_input_details()
  interpreter.set_tensor(input_details[0]["index"], preprocessed_style_image)

  # Calculate style bottleneck.
  interpreter.invoke()
  style_bottleneck = interpreter.tensor(
      interpreter.get_output_details()[0]["index"]
      )()

  return style_bottleneck

# Run style transform on preprocessed style image
def run_style_transform(style_bottleneck, preprocessed_content_image):
  # Load the model.
  interpreter = tf.lite.Interpreter(model_path=style_transform_path)

  # Set model input.
  input_details = interpreter.get_input_details()
  interpreter.allocate_tensors()

  # Set model inputs.
  interpreter.set_tensor(input_details[0]["index"], preprocessed_content_image)
  interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
  interpreter.invoke()

  # Transform content image.
  stylized_image = interpreter.tensor(
      interpreter.get_output_details()[0]["index"]
      )()

  return stylized_image

# Function to prepare a plot for saving
def prepare_plot_for_saving():
    plt.axis('off')  # Hide the axes
    plt.gca().set_position([0, 0, 1, 1])  # Make the image fill the whole plot
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, 
                        hspace=0, wspace=0)  # Adjust the plot to fill the figure
    plt.margins(0,0)  # Remove any margins

# Function to save a plot to a file
def save_plot(directory, filename):
    # Create the full path by combining the directory and filename
    full_path = os.path.join(directory, filename)

    # Ensure the directory exists, create if it does not
    os.makedirs(directory, exist_ok=True)

    # Save the figure to the constructed path
    plt.savefig(full_path)
    plt.close()  # Close the plot after saving to free up resources



# Function to perform style transfer
def perform_style_transfer(content_path, style_path):
    # Load the input images.
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    # Preprocess the input images.
    preprocessed_content_image = preprocess_image(content_image, 384)
    preprocessed_style_image = preprocess_image(style_image, 256)

    ##############################################################################
    # 1st Run: Stylize the content image using the style bottleneck.
    # Calculate style bottleneck for the preprocessed style image.
    style_bottleneck = run_style_predict(preprocessed_style_image)

    # Stylize the content image using the style bottleneck.
    stylized_image = run_style_transform(style_bottleneck, preprocessed_content_image)

    # Prepare and save the stylized image
    imshow(stylized_image, 'Stylized Image')
    prepare_plot_for_saving()
    save_plot(os.path.join(img_path, 'result'), stylized_fn)

    ##############################################################################
    # 2nd Run: Stylize the content image using the style bottleneck of the content image.
    # Calculate style bottleneck of the content image.
    style_bottleneck_content = run_style_predict(
        preprocess_image(content_image, 256)
        )

    # Define content blending ratio between [0..1].
    # 0.0: 0% style extracts from content image.
    # 1.0: 100% style extracted from content image.
    content_blending_ratio = 0.5

    # Blend the style bottleneck of style image and content image
    style_bottleneck_blended = content_blending_ratio * style_bottleneck_content + (1 - content_blending_ratio) * style_bottleneck

    # Stylize the content image using the style bottleneck.
    stylized_image_blended = run_style_transform(style_bottleneck_blended, preprocessed_content_image)

    # Prepare and save the blended image
    imshow(stylized_image_blended, 'Blended Image')
    prepare_plot_for_saving()
    save_plot(os.path.join(img_path, 'result'), blended_fn)
    
    stylized_url = os.path.join(base_url, stylized_image_path)
    blended_url = os.path.join(base_url, blended_image_path)
    return (stylized_url, blended_url)