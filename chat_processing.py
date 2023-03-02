import time
import pythainlp
import numpy as np

from tensorflow import keras

from utils.logger import info_log
from utils.loader import load_parquet_intents, load_label_encoder, load_keras_model, get_model_version

MAX_LENGTH = 20

model_version = get_model_version('./model')

data = load_parquet_intents(f'./model/model_v{model_version}/intents.parquet')

label_encoder = load_label_encoder(f'./model/model_v{model_version}/label_encoder.pickle')
word_encoder = load_label_encoder(f'./model/model_v{model_version}/word_label_encoder.pickle')

model = load_keras_model(f'./model/model_v{model_version}/chat_model')

def to_sequences(message: str) -> list[int]:
    msg = pythainlp.word_tokenize(message, keep_whitespace = False)
    return word_encoder.transform(msg)


def process_message(message: str, debug: bool = False) -> str:

    message = message.lower()

    start = time.perf_counter()
    
    try:
        sequence = to_sequences(message)

    except ValueError:

        end = time.perf_counter()

        if debug:
            info_log(f'Time elasped: {round((end - start) * 1000, 4)} ms')
            info_log('Response with intents: *unknown intents*')
            info_log(f'In: {pythainlp.word_tokenize(message, keep_whitespace = False)}')

        return 'I think I don\'t know this.'
    
    result = model.predict(keras.preprocessing.sequence.pad_sequences([sequence], truncating = 'post', maxlen = MAX_LENGTH))
    tag = label_encoder.inverse_transform([np.argmax(result)])

    for intents in data:
        if intents['tag'] == tag:
            response = np.random.choice(intents["responses"])

    end = time.perf_counter()

    if debug:
        info_log(f'Time elasped: {round((end - start) * 1000, 4)} ms')
        info_log(f'Response with intents: "{label_encoder.inverse_transform([np.argmax(result)])[0]}"')
        info_log(f'In: {pythainlp.word_tokenize(message, keep_whitespace = False)}')

    return response