from PIL import Image
import requests
from io import BytesIO
from dotenv import load_dotenv
import os
from openai import OpenAI

def print_env_file_contents():
    """
    Prints the contents of the .env file to the console.
    """
    # Attempt to print environment variables; useful for debugging
    print("Environment Variables:")
    for key in os.environ:
        print(f"{key}: {os.environ[key]}")

def generate_style_image(description, output_path="static/images/style/generated.png"):
    """
    Generate a style image from a text description using OpenAI's API, designed to create abstract and
    highly stylized images suitable for use as style images in style transfer.
    """
    prompt = f"Create a highly abstract and stylized painting that visually represents the theme of the following prompt, be sure to use exaggerated colors and shapes that really highlight the unique mood and style that the prompt warrants, make it a suitable image to use as the style image in style transfer. Do NOT use too many lines, geometric shapes are good, emphasize color schemes and shape patterns. Really represent how the prompt FEELS: {description}"

    # Load .env variables if available; not strictly necessary in Docker if env_file is used
    load_dotenv()  # It will look for an .env file in the working directory by default or use the absolute path if needed

    # Debug print to check environment variables
    print('Loaded Environment Variables (debug print):')
    print_env_file_contents()

    # Access API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Please check your environment configuration.")

    client = OpenAI(api_key=api_key)

    response = client.images.generate(
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    image_response = requests.get(image_url)

    image = Image.open(BytesIO(image_response.content))
    image.save(output_path)
    return output_path
