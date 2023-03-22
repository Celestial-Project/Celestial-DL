import os
import pickle
import tensorflow
import pandas as pd

from sklearn.preprocessing import LabelEncoder

from utils.logger import error_log

def _add_responses(chat: dict, response: dict) -> dict:

    if response and chat:
        chat['responses'] = response
    
    return chat


def load_parquet_intents(path: str) -> list[dict]:
    
    data = pd.read_parquet(path, columns = ['intents_en', 'intents_th', 'fes_res_en', 'fes_res_th'])
    
    data['intents_en'] = data.apply(lambda row: _add_responses(row['intents_en'], row['fes_res_en']), axis = 1)
    data['intents_th'] = data.apply(lambda row: _add_responses(row['intents_th'], row['fes_res_th']), axis = 1)
    
    chat_list = data['intents_en'].tolist() + data['intents_th'].tolist()
    return [chat for chat in chat_list if chat]
    

def load_label_encoder(path: str) -> LabelEncoder:
    with open(path, 'rb') as enc:
        return pickle.load(enc)
    
    
def load_keras_model(path: str) -> tensorflow.keras.models.Sequential:
    return tensorflow.keras.models.load_model(path)


def get_model_version(model_path: str) -> int:
    
    detected_path = [dir for dir in os.listdir(model_path) if not dir.endswith('.zip') and dir != '.DS_Store']
    
    if not detected_path:
        error_log('Exception detected: The chat model directory is not found (If you have already download the model, please extract it to the model folder.)')
        return
    
    return max([int(dir[7:]) for dir in detected_path])