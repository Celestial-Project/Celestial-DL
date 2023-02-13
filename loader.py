import json
import pickle
import tensorflow

from sklearn.preprocessing import LabelEncoder

def load_json(path: str) -> dict:
    with open(path, encoding = 'utf-8') as f:
        return json.load(f)
    

def load_label_encoder(path: str) -> LabelEncoder:
    with open(path, 'rb') as enc:
        return pickle.load(enc)
    
    
def load_keras_model(path: str) -> tensorflow.keras.models.Sequential:
    return tensorflow.keras.models.load_model(path)