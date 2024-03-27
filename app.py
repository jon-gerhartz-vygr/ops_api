from auth import verify_key
from crud import update_user
from dotenv import load_dotenv
from flask import Flask, request, redirect, jsonify, url_for, make_response
import os
from utils import get_public_ip

load_dotenv()

# load env vars
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

ip = get_public_ip()
print(ip)


@app.route('/update_user', methods=['POST'])
def request_user_update():
    api_key = request.headers.get('Authorization').split()[1]
    if not verify_key(api_key):
        status_code = 404
        message = 'Unauthorized'
    else:
        user_id = request.args.get('user_id')
        data = request.get_json()
        resp = update_user(user_id, data)
        if resp['status'] == 'complete':
            status_code = 200
        else:
            status_code = 500
    return make_response(jsonify(resp['message']), status_code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
