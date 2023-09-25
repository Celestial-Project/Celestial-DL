import os

def info_log(log_message: str) -> None:
    print(f'\u001b[45;1m ** \u001b[0m {log_message}')


def error_log(log_message: str) -> None:
    print(f'\u001b[41;1m !! \u001b[0m {log_message}')
    
    
def incoming_log(log_message: str) -> None:
    print(f'\u001b[42;1m -> \u001b[0m {log_message}')


def outgoing_log(log_message: str) -> None:
    print(f'\u001b[41;1m <- \u001b[0m {log_message}')


def clear_log() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')