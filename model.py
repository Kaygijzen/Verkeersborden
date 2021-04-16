import os
import cv2
from tensorflow import keras
import numpy as np

MODEL_LOC = './model/Model7_Batch32_zoom.h5'
CLASSES = ['A01-100', 'A01-50', 'A01-30']

model = keras.models.load_model(MODEL_LOC)


def prepare(filepath):
    img_array = cv2.imread(filepath)
    new_array = cv2.resize(img_array, (112, 112), 3)
    return new_array.reshape(-1, 112, 112, 3)


def predict_images(folderPath):
    predictions = []
    files = os.listdir(folderPath)
    for file in files:
        imgPath = folderPath + file
        prediction = model.predict([prepare(imgPath)])
        maxPred = max(prediction[0])
        x = np.where(prediction[0] == maxPred)
        x = x[0][0]

        predictions.append([file, CLASSES[x]])
    return predictions