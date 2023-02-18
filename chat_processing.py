import time
import pythainlp
import numpy as np

from tensorflow import keras

from loader import load_json, load_label_encoder, load_keras_model, get_model_version

MAX_LENGTH = 20

model_version = get_model_version('./model')

data1 = load_json('./data/intents_th.json')
data2 = load_json('./data/intents_en.json')

label_encoder = load_label_encoder(f'./model/model_v{model_version}/label_encoder.pickle')
word_encoder = load_label_encoder(f'./model/model_v{model_version}/word_label_encoder.pickle')

data = data1['intents_th'] + data2['intents_en']
model = load_keras_model(f'./model/model_v{model_version}/chat_model')

def to_sequences(message) -> list[int]:
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
            print(f'\u001b[45;1m ** \u001b[0m Time elasped: {round((end - start) * 1000, 4)} ms')
            print(f'\u001b[45;1m ** \u001b[0m Response with intents: *unknown intents*')
            print(f'\u001b[45;1m ** \u001b[0m In: {pythainlp.word_tokenize(message, keep_whitespace = False)}')

        return 'I think I don\'t know this.'
    
    result = model.predict(keras.preprocessing.sequence.pad_sequences([sequence], truncating = 'post', maxlen = MAX_LENGTH))
    tag = label_encoder.inverse_transform([np.argmax(result)])

    for intents in data:
        if intents['tag'] == tag:
            response = np.random.choice(intents["responses"])

    end = time.perf_counter()

    if debug:
        print(f'\u001b[45;1m ** \u001b[0m Time elasped: {round((end - start) * 1000, 4)} ms')
        print(f'\u001b[45;1m ** \u001b[0m Response with intents: "{label_encoder.inverse_transform([np.argmax(result)])[0]}"')
        print(f'\u001b[45;1m ** \u001b[0m In: {pythainlp.word_tokenize(message, keep_whitespace = False)}')

    return response