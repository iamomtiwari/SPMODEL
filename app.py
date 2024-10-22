from flask import Flask, request, render_template
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)

# Load your model
model_path = os.path.join('model', 'finetuned_vit_model.pth')
model = load_model(model_path)

# Class labels
class_labels = [
    "Corn___Common_Rust",
    "Corn___Gray_Leaf_Spot",
    "Corn___Healthy",
    "Corn___Northern_Leaf_Blight",
    "Rice___Brown_Spot",
    "Rice___Healthy",
    "Rice___Leaf_Blast",
    "Rice___Neck_Blast",
    "Wheat___Brown_Rust",
    "Wheat___Healthy",
    "Wheat___Yellow_Rust",
    "Sugarcane__Red_Rot",
    "Sugarcane__Healthy",
    "Sugarcane__Bacterial Blight"
]

# Solutions dictionary
solutions = {
    "Corn___Healthy": "Continue monitoring. Ensure proper water and nutrient supply.",
    "Corn___Common_Rust": "Monitor the spread. Apply fungicides if necessary.",
    "Corn___Gray_Leaf_Spot": "Rotate crops and apply appropriate fungicides.",
    "Corn___Northern_Leaf_Blight": "Remove infected leaves and apply fungicides.",
    # Add other classes and their solutions here...
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        img_file = request.files['image']
        if img_file:
            img_path = os.path.join('static', img_file.filename)
            img_file.save(img_path)

            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            predictions = model.predict(img_array)
            predicted_class = class_labels[np.argmax(predictions)]
            solution = solutions.get(predicted_class, "No solution available.")

            return render_template('index.html', predicted_class=predicted_class, solution=solution)

if __name__ == '__main__':
    app.run(debug=True)
