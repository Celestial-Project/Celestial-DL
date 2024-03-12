import time

from typing import Callable
from functools import wraps

from utils.logger import info_log, error_log

def retry(attempts: int = 3, delay: float = 1, debug: bool = False) -> Callable:
    
    if attempts < 1:
        raise ValueError('Retry Error: a number of attempts must be equal or greater than one')
    
    if delay <= 0:
        raise ValueError('Retry Error: a delay interval must be greater than zero')
    
    def decorator(function: Callable) -> Callable:
        
        @wraps(function)
        def wrapper(*args, **kwargs) -> any:
            
            for n_retry in range(1, attempts + 1):
                
                try:
                    if not debug:
                        return function(*args, **kwargs)
                    
                    info_log(f'Attempt #{n_retry} of running {function.__name__}()')
                    return function(*args, **kwargs)
                    
                except Exception as e:
                    
                    if n_retry != attempts:
                        error_log(f'Error occured while executing {function.__name__}() -> {e}.')
                        time.sleep(delay)
                        continue
                        
                    error_log(f'Error occured while executing {function.__name__}() -> {e}.')
                    error_log(f'{function.__name__}() failed after {attempts} attempts.')
                    break
                
        return wrapper
    
    return decorator