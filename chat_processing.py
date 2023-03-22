import re
import json
import time
import pythainlp
import numpy as np
import datetime as dt

from tensorflow import keras

from utils.logger import info_log, incoming_log, outgoing_log
from utils.loader import load_parquet_intents, load_label_encoder, load_keras_model, get_model_version

MAX_LENGTH = 20

model_version = get_model_version('./model') if get_model_version('./model') else exit(1)

data = load_parquet_intents(f'./model/model_v{model_version}/intents.parquet')

label_encoder = load_label_encoder(f'./model/model_v{model_version}/label_encoder.pickle')
word_encoder = load_label_encoder(f'./model/model_v{model_version}/word_label_encoder.pickle')

model = load_keras_model(f'./model/model_v{model_version}/chat_model')

with open('./data/unknown_responses.json', encoding = 'utf-8') as f:
    unknown_responses = json.load(f)

def detect_thai(list_of_words: list[str]) -> bool:
    
    '''
        Determine of the list of string is Thai or not
    '''
    
    regexp = re.compile(rf'[{pythainlp.thai_characters}]')
    thai_prob = sum(1 for word in list_of_words if regexp.search(word))
    percentage = round((thai_prob / len(list_of_words)) * 100, 2)
    
    return percentage >= 50


def to_sequences(list_of_words: list[str]) -> list[int]:
    return word_encoder.transform(list_of_words)


def process_message(message: str, debug: bool = False) -> str:

    start = time.perf_counter()

    message = message.lower()
    tokenized_text = pythainlp.word_tokenize(message, keep_whitespace = False)
    
    current_date = dt.date.today()

    is_thai = detect_thai(tokenized_text)
    
    try:
        sequence = to_sequences(tokenized_text)

    except ValueError:

        response = np.random.choice(unknown_responses['th'] if is_thai else unknown_responses['en'])

        end = time.perf_counter()

        if debug:
            info_log(f'Time elasped: {round((end - start) * 1000, 4)} ms')
            incoming_log(f'In: {pythainlp.word_tokenize(message, keep_whitespace = False)}')
            outgoing_log('Response with intents: *unknown intents*')
            outgoing_log(response)

        return response
    
    result = model.predict(keras.preprocessing.sequence.pad_sequences([sequence], truncating = 'post', maxlen = MAX_LENGTH))
    tag = label_encoder.inverse_transform([np.argmax(result)])

    for intents in data:
        
        if intents['tag'] == tag:
            
            if intents['month']:
                
                festival_date = intents['date'].astype(np.int64)
                festival_month = int(intents['month'])
                
                if len(festival_date) == 1:
                    festival_date = festival_date[0]
                    date_frame = [dt.datetime(current_date.year, festival_month, festival_date).date()]
                
                elif len(festival_date) == 2:
                    date_range = range(festival_date[0], (festival_date[1] + 1))
                    date_frame =  [dt.datetime(current_date.year, festival_month, d).date() for d in date_range]
                    
                response = np.random.choice(intents['responses']['fes' if current_date in date_frame else 'nonfes'])
                
            elif not intents['month']:
                response = np.random.choice(intents['responses'])

    end = time.perf_counter()

    if debug:
        info_log(f'Time elasped: {round((end - start) * 1000, 4)} ms')
        incoming_log(f'In: {pythainlp.word_tokenize(message, keep_whitespace = False)}')
        outgoing_log(f'Response with intents: "{label_encoder.inverse_transform([np.argmax(result)])[0]}"')
        outgoing_log(response)

    return response