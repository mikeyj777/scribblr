import os
import json

keras_config_path = os.path.join(os.path.expanduser('~'), '.keras', 'keras.json')

if os.path.exists(keras_config_path):
    with open(keras_config_path, 'r') as f:
        config = json.load(f)
    
    # Change the backend to TensorFlow
    config['backend'] = 'tensorflow'
    
    with open(keras_config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    print("Keras config updated to use TensorFlow backend.")
else:
    print("No Keras config file found. Creating one with TensorFlow backend.")
    config = {
        "floatx": "float32",
        "epsilon": 1e-07,
        "backend": "tensorflow",
        "image_data_format": "channels_last"
    }
    os.makedirs(os.path.dirname(keras_config_path), exist_ok=True)
    with open(keras_config_path, 'w') as f:
        json.dump(config, f, indent=4)

print("Current Keras config:")
with open(keras_config_path, 'r') as f:
    print(f.read())