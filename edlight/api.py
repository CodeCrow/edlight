"""
API endpoint for maths application
"""
import base64
import openai
import requests
from django.conf import settings
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

openai.api_key = settings.OPENAI_KEY
api = NinjaAPI()


@api.post("analyze/")
def analyze(request, file: UploadedFile = File(...)) -> dict:
    """
    handle api request and response
    """
    # encode the image to send it to the api 
    base64_image = base64.b64encode(file.read()).decode('utf-8')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()
