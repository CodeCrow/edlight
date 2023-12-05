"""
API endpoint for maths application
"""
import base64
import json
import openai
import magic
import requests
from django.conf import settings
from django.http import HttpResponse
from ninja import File, NinjaAPI
from ninja.errors import HttpError, ValidationError
from ninja.files import UploadedFile

openai.api_key = settings.OPENAI_KEY
api = NinjaAPI()

allowed_images = ('jpeg', 'gif', 'png', )


@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse(exc.errors, status=422)  


@api.post("analyze/")
def analyze(request, file: UploadedFile = File(...)) -> dict:
    """
    handle api request and response
    """

    openai_error_status = 500
    # check the file type
    buffered_file = file.read()

    major, minor = magic.from_buffer(buffered_file, mime=True).split("/")
    if major != 'image':
        raise ValidationError("Uploaded file must be an image.")
    
    if minor not in allowed_images:
        raise ValidationError(f"Uploaded file must be an image of types {(', ').join(allowed_images)}.")

    # encode the image to send it to the api 
    base64_image = base64.b64encode(buffered_file).decode('utf-8')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_KEY}"
    }

    payload = {
        "model": f"{settings.OPENAI_MODEL}",
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
        "max_tokens": 1000
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    except requests.exceptions.ConnectionError:
        # this could be updated to wait and then retry
        openai_error_status = 503
        raise HttpError(openai_error_status, "The OpenAI service is currently unreachable.  Try again later")
    except requests.exceptions.HTTPError:
        openai_error_status = 500
        raise HttpError(openai_error_status, "The OpenAI service has returned an invalid response.")
    except requests.exceptions.Timeout:
        openai_error_status = 504
        raise HttpError(openai_error_status, "The OpenAI service has has timed out.  Try again later.")
    response_json = response.json()
    if response_json.get('error', None):
        if response_json['error'].get('type') == "server_error":
            openai_error_status = 503
            raise HttpError(openai_error_status, response_json['error'].get('message', "An unknown error has occured."))
        if response_json['error'].get('code') == "invalid_api_key":
            openai_error_status = 403
            raise HttpError(openai_error_status, response_json['error'].get('message', "You do not have a valid API key to access OpenAI"))
        # there was an error but we don't know what it was
        raise HttpError(openai_error_status, f"An unknown error has occured when accessing OpenAI. {response_json.get('error')}")
    # process the response
    try:
        response_json = response.json()
        return {'description': response_json['choices'][0]['message']['content']}
    except:
        # problem with the response.
        # Specifically, something has gone wrong with the expected json:
        # wrong attributes, bad formatting.
        # something unexpected, but that OpenAI thinks is right.
        openai_error_status = 500
        raise HttpError(openai_error_status, "The OpenAI service has returned an invalid response.")

    return response.json()
