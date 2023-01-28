import json 
import pickle
import pythainlp
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

with open('./data/intents_th.json', encoding = 'utf-8') as f:
    data1 = json.load(f)

with open('./data/intents_en.json', encoding = 'utf-8') as f:
    data2 = json.load(f)

data = data1['intents_th'] + data2['intents_en']

training_sentences = []
training_labels = []
labels = []
responses = []

for intent in data:
    
    for pattern in intent['patterns']:
        training_sentences.append(pattern.lower())
        training_labels.append(intent['tag'])
    
    responses.append(intent['responses'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag'])
        
num_classes = len(labels)

wordlist = [pythainlp.word_tokenize(seq, engine = 'nercut', keep_whitespace = False) for seq in training_sentences]
wordset = list(set([j for i in wordlist for j in i]))

label_encoder = LabelEncoder()
label_encoder.fit(training_labels)

training_labels = label_encoder.transform(training_labels)

word_label_encoder = LabelEncoder()
word_label_encoder.fit(wordset)

encoded_sentences = pad_sequences([word_label_encoder.transform(wl) for wl in wordlist], truncating = 'post', maxlen = 20)

max_length = 20
model = Sequential()

model.add(Embedding(len(wordset), 16, input_length = 20))
model.add(GlobalAveragePooling1D())
model.add(Dense(16, activation = 'relu'))
model.add(Dense(16, activation = 'relu'))
model.add(Dense(16, activation = 'relu'))
model.add(Dense(num_classes, activation = 'softmax'))

model.compile(loss = 'sparse_categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
model.fit(encoded_sentences, np.array(training_labels), epochs = 800)

model.save("./model/chat_model")

with open('./model/label_encoder.pickle', 'wb') as ecn_file:
    pickle.dump(label_encoder, ecn_file, protocol = pickle.HIGHEST_PROTOCOL)

with open('./model/word_label_encoder.pickle', 'wb') as ecn_file:
    pickle.dump(word_label_encoder, ecn_file, protocol = pickle.HIGHEST_PROTOCOL)