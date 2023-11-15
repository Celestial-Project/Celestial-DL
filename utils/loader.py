import os
import pickle
import tensorflow
import pandas as pd
import pyarrow as pa

from sklearn.preprocessing import LabelEncoder

from utils.logger import error_log

def __add_responses(chat: dict, response: dict) -> dict:

    if response and chat:
        chat['responses'] = response
    
    return chat


def load_parquet_intents(path: str) -> list[dict]:
    
    try:
        data = pd.read_parquet(path, columns = ['intents_en', 'intents_th', 'fes_res_en', 'fes_res_th'])

    except pa._lib.ArrowInvalid:
        error_log('Exception detected: Your model is older than v7 which is not compatable with our current chat processing module.')
        return
    
    data['intents_en'] = data.apply(lambda row: __add_responses(row['intents_en'], row['fes_res_en']), axis = 1)
    data['intents_th'] = data.apply(lambda row: __add_responses(row['intents_th'], row['fes_res_th']), axis = 1)
    
    chat_list = data['intents_en'].tolist() + data['intents_th'].tolist()
    return [chat for chat in chat_list if chat]
    

def load_label_encoder(path: str) -> LabelEncoder:
    with open(path, 'rb') as enc:
        return pickle.load(enc)
    
    
def load_keras_model(path: str) -> tensorflow.keras.models.Sequential:
    return tensorflow.keras.models.load_model(path)


def get_latest_model(model_path: str) -> str:
    
    detected_path = [dir for dir in os.listdir(model_path) if not dir.endswith('.zip') and dir != '.DS_Store']
    
    if not detected_path:
        error_log('Exception detected: The chat model directory is not found (If you have already download the model, please extract it to the model folder.)')
        exit(1)
    
    last_trained_date = [os.path.getmtime(f'./model/{dir}/chat_model') for dir in detected_path]
    last_trained = {k:v for (k, v) in zip(last_trained_date, detected_path)}
    
    return last_trained[last_trained_date[-1]]


def load_chat_model(model_name: str = get_latest_model('./model')) -> tuple:

    selectable_model = [path.name for path in os.scandir('./model') if path.is_dir()]
    
    if model_name not in selectable_model:
        error_log(f'Error: model "{model_name}" does not exist.')
        exit(1)

    data = load_parquet_intents(f'./model/{model_name}/intents.parquet')

    label_encoder = load_label_encoder(f'./model/{model_name}/label_encoder.pickle')
    word_encoder = load_label_encoder(f'./model/{model_name}/word_label_encoder.pickle')

    model = load_keras_model(f'./model/{model_name}/chat_model')

    return (model, model_name, data, label_encoder, word_encoder)