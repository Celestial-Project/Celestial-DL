import os

from datetime import datetime as dt

from utils.loader import load_chat_model
from utils.logger import info_log, incoming_log, error_log

from chat_processing import process_message

# run this file to test your chat intents on the terminal before commit
(model, model_name, data, label_encoder, word_encoder) = load_chat_model()

os.system('cls' if os.name == 'nt' else 'clear')

info_log('Welcome to Celestial command-line testing interface!')
info_log('Type -h or --help to see list of test macro and controls.')
info_log('Press ctrl+c to exit.')

def read_input(message: str) -> None:

    '''
        Process the input message and take appropriate action.
    '''

    global model, model_name, data, label_encoder, word_encoder
    
    if not message:
        return

    if message in {'--help', '-h'}:

        print('\u001b[43;1m macro \u001b[0m -h  --help \t\t Show this help message.')
        print('\u001b[43;1m macro \u001b[0m -mi --model-info \t Show model info.')
        print('\u001b[43;1m macro \u001b[0m -ms --model-swap \t Swap model.')
        print('\u001b[41;1m  ctl  \u001b[0m ^C ctrl+c \t\t Quit the program.')
        print('\u001b[41;1m  ctl  \u001b[0m ^D ctrl+d \t\t Quit the program.')

        return
    
    elif message in {'--model-swap', '-ms'}:
        
        selectable_model = [path.name for path in os.scandir('./model') if path.is_dir()]
        
        info_log('Selectable model:')
        info_log(", ".join(selectable_model))

        incoming_log('Please select a model')
        selected_model = input('\u001b[47;1m MS \u001b[0m ').strip()

        if selected_model not in selectable_model:
            error_log(f'Error: model "{selected_model}" does not exist.')
            return

        (model, model_name, data, label_encoder, word_encoder) = load_chat_model(selected_model)

        os.system('cls' if os.name == 'nt' else 'clear')

        info_log(f'Current model: {model_name}')

        return

    elif message in {'--model-info', '-mi'}:

        last_trained_date = dt.fromtimestamp(os.path.getmtime(f'./model/{model_name}/chat_model'))

        info_log(f'Model name: {model_name}')
        info_log(f'Last trained: {last_trained_date.strftime("%d %B %Y")} ({last_trained_date.time().strftime("%H:%M:%S")})')
        info_log(f'Model path: {os.path.abspath(f"./model/{model_name}")}')

        return

    process_message(message, model, data, label_encoder, word_encoder, debug = True)


while True:
    
    try:
        inp = input('\u001b[47;1m #> \u001b[0m ').strip()
        read_input(inp)
        
    except (KeyboardInterrupt, EOFError):
        print()
        info_log('Exiting test mode...')
        exit()