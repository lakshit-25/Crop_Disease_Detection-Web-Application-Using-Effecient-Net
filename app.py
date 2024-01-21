from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
import joblib
import cv2

app = Flask(__name__)

# Load the pre-trained model and label binarizer
model = load_model('plant_disease_model.h5')  # Replace 'your_model.h5' with the actual file name
label_binarizer = joblib.load('label_transform.pkl')  # Replace 'label_transform.pkl' with the actual file name

def convert_image_to_array(image_path):
    try:
        image = cv2.imread(image_path)
        if image is not None:
            image = cv2.resize(image, (224, 224))
            return np.expand_dims(image, axis=0)
        else:
            return np.array([])
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get the uploaded image
            file = request.files['file']
            
            # Save the uploaded image
            image_path = 'static/uploads/' + file.filename
            file.save(image_path)

            # Convert the image to array
            image_array = convert_image_to_array(image_path)

            # Make prediction
            prediction = model.predict(image_array)
            
            # Convert one-hot encoded prediction to class label
            predicted_label = label_binarizer.inverse_transform(prediction)[0]

            return render_template('result.html', prediction=predicted_label, image_path=image_path)

        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
