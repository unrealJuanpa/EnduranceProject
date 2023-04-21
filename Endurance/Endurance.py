# natural language processing
import nltk
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("spanish")

# reconocimiento de voz
import speech_recognition as sr
import time
import pyaudio
recognizer_instance = sr.Recognizer()

# serial port
import serial, time

# red neuronal profunda
import numpy as np
import tflearn
import tensorflow as tf
import random

# Modulo de habla
import win32com.client
speaker = win32com.client.Dispatch("SAPI.SpVoice")

print("Importando datos . . .")
# importacion dataset de Hall
import json
with open('data.json') as json_data:
    intents = json.load(json_data)

words = []
classes = []
documents = []
ignore_words = ['?']

def limpiar(str3):
    str3 = str3.replace("!", "")
    str3 = str3.replace('\n', "")
    str3 = str3.replace('\t', "")
    str3 = str3.replace("¡", "")
    str3 = str3.replace("?", "")
    str3 = str3.replace("¿", "")
    str3 = str3.replace("á", "a")
    str3 = str3.replace("é", "e")
    str3 = str3.replace("í", "i")
    str3 = str3.replace("ó", "o")
    str3 = str3.replace("ú", "u")
    return str3

# se repite mientra haya algo que explorar
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokeniza cada palabra de la frase
        w = nltk.word_tokenize(pattern)
        # lo agrega a la lista de palabras
        words.extend(w)
        # agrega al corpus
        documents.append((w, intent['tag']))
        # agrega la clase correspondiente
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# normaliza las palabras y ve si no hay repetidas
Swords = [stemmer.stem(pal.lower()) for pal in words]
words = sorted(list(set(Swords)))

# quita duplicados
classes = sorted(list(set(classes)))

print(len(documents), "documentos")
print(len(classes), "clases", classes)
print(len(words), "palabras unicas normalizadas", words)

# traduccion de datos (palabras a tensores de numeros)
training = []
output = []

# se crea un vector vacio para nuestras salida
output_empty = [0]* len(classes)

# datos de entrenamiento, bolsa de palabras para cada oracion
for doc in documents:
    # inicializa nuestra bolsa de palabras
    bag = []
    # lista de las palabras tokenizadas para las coincidencias
    pattern_words = doc[0]
    # trabaja cada palabra
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # crea nuestro vector de bolsa de palabras
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    # la salida es 0 para cada tag, y 1 para el tag actual
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# buferar nuestras caracteristicas y pone en el np vector
random.shuffle(training)
training = np.array(training)

# crea las listas de entrenamiento y de test
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Entrada: ", train_x)
print("Salida: ", train_y)
print("Iniciando arquitectura de la red . . .")
# resetea graficos de datos subyacentes
tf.reset_default_graph()
# construccion de la red neuronal

capa = tflearn.input_data(shape=[None, len(train_x[0])])
capa = tflearn.fully_connected(capa, 10, activation='linear')
capa = tflearn.fully_connected(capa, 9, activation='leaky_relu')
capa = tflearn.fully_connected(capa, 13, activation='leaky_relu')
capa = tflearn.fully_connected(capa, len(train_y[0]), activation='softmax')
capa = tflearn.regression(capa, optimizer='adam')

# define nuestro modelo y ajusta tensorboard
model = tflearn.DNN(capa, tensorboard_dir='tflearn_logs')
# inicia el entrenamiento (aplicando el algoritmo de decenso del gradiente ADAM)
print("Iniciando entrenamiento . . .")
model.fit(train_x, train_y, n_epoch=1400, batch_size=8, show_metric=True)

# ------------------ aqui se puede guardar ---------------------

with open('data.json') as json_data:
    intents = json.load(json_data)

def clean_up_sentence(sentence):
    # tokeniza la entrada
    sentence_words = nltk.word_tokenize(sentence)
    print("Token original: ", sentence_words)
    # trabaja cada palabra
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# retorna el vector correspondiente a la bolsa de palabras

def bow(sentence, words, show_details=True):
    # tokeniza la peticion
    
    sentence_words = clean_up_sentence(sentence)
    print("Final token: ", sentence_words)
    # bolsa de palabras
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("Perteneciente a: %s" % w)

    return(np.array(bag))

context = {}
ERROR_THRESHOLD = 0.25

def classify(sentence):
    # genera las probabilidades del modelo
    print("Funcion Bow: ", bow(sentence, words))
    results = model.predict([bow(sentence, words)])[0]
    print("Prediccion del modelo: ", results)
    # filtra las probabilidades fuera del preset error
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # ordena por la probabilidad
    results.sort(key=lambda x: x[1], reverse=True)
    print("Mejor probabilidad: ", results[0])
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # retorna la lista ordenada de las peticiones y su probabilidad
    return return_list

def response(sentence, userID='123', show_details=True):
    results = classify(sentence)
    print(results)
    # si tenemos una clasificacion que contenga a la peticion en si
    if results:
        # repite siempre que hayan coincidencias para procesar
        while results:
            for i in intents['intents']:
                # encuentra una etiqueta que coincida con el primer resultado
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('Contexto:', i['context_set'])
                        context[userID] = i['context_set']

                    # ve si hay contexto o no
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('Interpretacion:', i['tag'])
                        st1 = random.choice(i['responses'])
                        return st1

            results.pop(0)

while 1:
    text = input(">>> ")
    print("HALL: ", response(limpiar(text)))
    
    
# ver archivo de texto en escritorio