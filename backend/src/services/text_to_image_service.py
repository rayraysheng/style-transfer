import openai
from PIL import Image
import requests
from io import BytesIO

def generate_style_image(description, output_path="./static/images/style/generated.png"):
    """
    Generate a style image from a text description using OpenAI's API, designed to create abstract and
    highly stylized images suitable for use as style images in style transfer.
    """
    prompt = f"Create a highly abstract and stylized painting that visually represents the theme: {description}"

    response = openai.Image.create(
        model="text2im-002",
        prompt=prompt,
        size="256x256",
        n=1
    )

    image_url = response['data'][0]['url']
    image_response = requests.get(image_url)

    image = Image.open(BytesIO(image_response.content))
    image.save(output_path)
    return output_path
