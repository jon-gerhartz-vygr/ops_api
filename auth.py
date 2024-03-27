from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


def verify_key(key):
    if key == API_KEY:
        return True
    else:
        return False
