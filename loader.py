import os
import pickle
import tensorflow
import pandas as pd

from sklearn.preprocessing import LabelEncoder

def load_parquet_intents(path: str) -> list[dict]:
    
    data = pd.read_parquet(path)
    chat_list = list(data['intents_en']) + list(data['intents_th'])
    
    return [chat for chat in chat_list if chat]
    

def load_label_encoder(path: str) -> LabelEncoder:
    with open(path, 'rb') as enc:
        return pickle.load(enc)
    
    
def load_keras_model(path: str) -> tensorflow.keras.models.Sequential:
    return tensorflow.keras.models.load_model(path)


def get_model_version(model_path: str) -> int:
    return max([int(dir[7:]) for dir in os.listdir(model_path) if not dir.endswith('.zip')])