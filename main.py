import json
import time
import pickle
import pythainlp
import numpy as np

from tensorflow import keras

MAX_LENGTH = 20

with open('./intents.json', encoding = 'utf-8') as f:
    data1 = json.load(f)

with open('./intents2.json', encoding = 'utf-8') as f:
    data2 = json.load(f)

with open('./model/label_encoder.pickle', 'rb') as enc:
    label_encoder = pickle.load(enc)

with open('./model/word_label_encoder.pickle', 'rb') as enc:
    word_encoder = pickle.load(enc)

data = data1['intents_th'] + data2['intents_en']
model = keras.models.load_model('./model/chat_model')

def to_sequences(message) -> list[int]:
    msg = pythainlp.word_tokenize(message, engine = 'nercut', keep_whitespace = False)
    return word_encoder.transform(msg)

while True:

    input_message = input('usr> ').lower()

    start = time.perf_counter()

    if input_message == 'quit':
        break
    
    try:

        sequence = to_sequences(input_message)
        print(sequence)
        
        result = model.predict(keras.preprocessing.sequence.pad_sequences([sequence], truncating = 'post', maxlen = MAX_LENGTH))
        print(np.argmax(result))

        tag = label_encoder.inverse_transform([np.argmax(result)])

        for i in data:
            if i['tag'] == tag:
                print(f'celestial: {np.random.choice(i["responses"])}')

    except ValueError as e:
        print('Unkown responses')
        print(e)

    end = time.perf_counter()

    elasped = start - end
    print(f'Time elasped: {round((end - start) * 1000, 4)} ms')