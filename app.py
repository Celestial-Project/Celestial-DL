import argparse

from flask import Flask, request
from flask_cors import CORS, cross_origin

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils.loader import load_chat_model
from utils.logger import info_log, clear_log
from utils.chat_processing import process_message

flags_parser = argparse.ArgumentParser(
    prog = 'Celestial API',
    description = 'A chat API service of Celestial project',
)

flags_parser.add_argument('-p', '--port', nargs = '?', default = 21250, type = int)
flags_parser.add_argument('-d', '--debug', action = 'store_true')
flags_parser.add_argument('-m', '--model', type=str)

args = flags_parser.parse_args()

debug = args.debug
PORT = args.port
selected_model = args.model

app = Flask(__name__)
cors = CORS(app)
limiter = Limiter(get_remote_address, app = app)

app.config['MAX_CONTENT_LENGTH'] = 1024

(model, model_name, data, label_encoder, word_encoder) = load_chat_model() if not selected_model else load_chat_model(selected_model)

def show_ready(port: int, debug: bool) -> None:

    clear_log()
    
    info_log('Chat REST API ready!')
    info_log(f'Model name: {model_name}')
    info_log(f'Mode: {"Debug" if debug else "Production"}')
    info_log('Press ctrl+c to exit.')
    info_log(f'API running on: http://localhost:{port}/chat-dl')


@cross_origin()
@limiter.limit('450/minute')
@app.route('/chat-dl', methods = ['POST'])
def send_response():
    
    body = request.get_json()
    
    if body is None or body['message'] == '':
        return ({}, 400)
    
    return ({'chat': process_message(body['message'], model, data, label_encoder, word_encoder, debug = debug)}, 200)


def main():

    process_message('hello', model, data, label_encoder, word_encoder)

    if debug:
        
        show_ready(PORT, debug)
        app.run(host = '0.0.0.0', port = PORT)
        
        return

    from waitress import serve

    show_ready(PORT, debug)
    serve(app, host = '0.0.0.0', port = PORT)
    

if __name__ == '__main__':
    main()