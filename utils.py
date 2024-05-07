from dotenv import load_dotenv
import os
import requests


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Error: Unable to fetch IP address"
    except Exception as e:
        return f"Exception occurred: {e}"


def write_log(type, identifier, identifier_type, message, meta_data):
    load_dotenv()
    SRVC_NAME = os.getenv("SRVC_NAME")
    LOGGER_URL = os.getenv("LOGGER_URL")
    API_KEY = os.getenv("API_KEY")

    headers = {"Authorization": f"Bearer {API_KEY}"}

    payload = {
        'type': type,
        'author_name': SRVC_NAME,
        'identifier': identifier,
        'identifier_type': identifier_type,
        'message': str(message),
        'meta_data': meta_data

    }
    resp = requests.post(LOGGER_URL, json=payload, headers=headers)
    print(resp.text)
