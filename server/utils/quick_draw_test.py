import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

# Load the pre-trained model
model = tf.keras.Sequential([
    hub.KerasLayer("https://tfhub.dev/google/quickdraw-classification/1")
])

# Function to preprocess the image
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = img.resize((28, 28))  # Resize to 28x28
    img_array = np.array(img, dtype=np.float32) / 255.0  # Normalize
    img_array = img_array.reshape((1, 28, 28, 1))  # Reshape for model input
    return img_array

# Function to classify the drawing
def classify_drawing(image_path):
    input_data = preprocess_image(image_path)
    predictions = model.predict(input_data)
    top_prediction = np.argmax(predictions[0])
    # You'll need to map this index to the actual class name
    return f"Top prediction: class index {top_prediction}"

# Example usage
print(classify_drawing('stick_figure.jpg'))