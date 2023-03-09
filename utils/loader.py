import os
import pickle
import tensorflow
import pandas as pd

from sklearn.preprocessing import LabelEncoder

from utils.logger import error_log

def load_parquet_intents(path: str) -> list[dict]:
    
    data = pd.read_parquet(path)
    
    list_en = list(data['intents_en'])
    list_th = list(data['intents_th'])
    
    for chat, response in zip(list_en, data['fes_res_en']):
        if response and chat:
            chat['responses'] = response
    
    for chat, response in zip(list_th, data['fes_res_th']):
        if response and chat:
            chat['responses'] = response
    
    chat_list = list_en + list_th
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
        exit(1)
    
    return max([int(dir[7:]) for dir in detected_path])