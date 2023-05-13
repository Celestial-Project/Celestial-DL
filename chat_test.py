import os

from datetime import datetime as dt

from utils.logger import info_log
from utils.loader import get_model_version

from chat_processing import process_message

# run this file to test your chat intents on the terminal before commit

os.system('cls' if os.name == 'nt' else 'clear')

info_log('Welcome to Celestial command-line testing interface!')
info_log('Type -h or --help to see list of test macro and controls.')
info_log('Press ctrl+c to exit.')

def read_input(message: str) -> None:

    '''
        Process the input message and take appropriate action.
    '''
    
    if not message:
        return

    if message in {'--help', '-h'}:

        print('''
            \u001b[43;1m macro \u001b[0m -h --help \t\t Show this help message.
            \u001b[41;1m  ctl  \u001b[0m ^C ctrl+c \t\t Quit the program.
            \u001b[41;1m  ctl  \u001b[0m ^D ctrl+d \t\t Quit the program.
        ''')

        return

    elif message in {'--model-info', '-mi'}:

        model_version = get_model_version('./model')
        last_trained_date = dt.fromtimestamp(os.path.getmtime(f'./model/model_v{model_version}/chat_model'))

        info_log(f'Model version: {model_version}')
        info_log(f'Last trained: {last_trained_date.strftime("%d %B %Y")} ({last_trained_date.time().strftime("%H:%M:%S")})')
        info_log(f'Model path: {os.path.abspath(f"./model/model_v{model_version}")}')

        return

    process_message(message, debug = True)


while True:
    
    try:
        inp = input('\u001b[47;1m #> \u001b[0m ').strip()
        read_input(inp)
        
    except (KeyboardInterrupt, EOFError):
        print()
        info_log('Exiting test mode...')
        exit()