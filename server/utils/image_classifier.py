import os
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.models import load_model

import tensorflow as tf

from pathlib import Path

parent = Path(__file__).parent.parent
data_path = os.path.join(parent, 'data')

custom_objects = {
    'GlorotUniform': tf.keras.initializers.GlorotUniform(),
    'Zeros': tf.keras.initializers.Zeros()
}

with tf.keras.utils.custom_object_scope(custom_objects):
    model = tf.keras.models.load_model(f'{data_path}/doodleNet-model.h5')

CLASSES = np.genfromtxt(f'{data_path}/class_names.txt', dtype=str)

def preprocess_image(image):

    image = image.resize((28, 28), resample=Image.BILINEAR)
    image = image.convert('L')  # convert to grayscale
    image_array = np.array(image).astype('float32') / 255.0
    image_array = np.expand_dims(image_array, axis=-1)
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def classify_image(image_path):
    image = Image.open(image_path)
    image_array = preprocess_image(image)
    predictions = model.predict(image_array)[0]
    top_indices = np.argsort(predictions)[::-1][:3]
    top_predictions = [(CLASSES[i], float(predictions[i])) for i in top_indices]
    return top_predictions