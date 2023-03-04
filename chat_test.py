import os

from utils.logger import info_log
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
                  
    process_message(message, debug = True)


while True:
    
    try:
        inp = input('\u001b[47;1m #> \u001b[0m ').strip()
        read_input(inp)
        
    except (KeyboardInterrupt, EOFError):
        print()
        info_log('Exiting test mode...')
        exit()