import os
from flask import Flask, request
from flask_cors import CORS, cross_origin

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils.logger import info_log
from chat_processing import process_message

debug = False

app = Flask(__name__)
cors = CORS(app)
limiter = Limiter(get_remote_address, app = app)

app.config['MAX_CONTENT_LENGTH'] = 1024

@cross_origin()
@limiter.limit('450/minute')
@app.route('/chat', methods = ['POST'])
def send_response():
    
    body = request.get_json()
    
    if body is None or body['message'] == '':
        return ({}, 400)
    
    return ({'chat': process_message(body['message'])}, 200)


def main():

    if debug:
        process_message('hello')
        app.run(host = '0.0.0.0', port = 21250)
        return

    from waitress import serve
    
    process_message('hello')
    
    os.system('cls' if os.name == 'nt' else 'clear')
    info_log('Chat REST API ready!')
    info_log('Press ctrl+c to exit.')
    info_log('API running on: http://localhost:21250')
    
    serve(app, host = '0.0.0.0', port = 21250)
    

if __name__ == '__main__':
    main()