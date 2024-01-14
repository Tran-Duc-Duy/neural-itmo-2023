import pyaudio
import numpy as np
import wave
from sklearn.preprocessing import StandardScaler
import time
from getfeature import get_features
from tensorflow.keras.models import load_model
import os
import joblib

emotions = ['disgust', 'happy', 'sad', 'neutral', 'fear', 'angry', 'surprise']
model = load_model('res_model.h5')

def emotion(features):
    scaler = joblib.load('scaler.pkl')
    features = features.reshape(1, -1)
    features = scaler.transform(features)
    features = np.expand_dims(np.array(features), axis=2)

    predictions = model.predict(features)[0]
    predicted_index = np.argmax(predictions)
    predicted_emotion = emotions[predicted_index]

    return predicted_emotion
