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
    "Corn___Common_Rust": "Apply fungicides as soon as symptoms are noticed. Practice crop rotation and remove infected plants.",
    "Corn___Gray_Leaf_Spot": "Rotate crops to non-host plants, apply resistant varieties, and use fungicides as needed.",
    "Corn___Healthy": "Continue good agricultural practices: ensure proper irrigation, nutrient supply, and monitor for pests.",
    "Corn___Northern_Leaf_Blight": "Remove and destroy infected plant debris, apply fungicides, and rotate crops.",
    "Rice___Brown_Spot": "Use resistant varieties, improve field drainage, and apply fungicides if necessary.",
    "Rice___Healthy": "Maintain proper irrigation, fertilization, and pest control measures.",
    "Rice___Leaf_Blast": "Use resistant varieties, apply fungicides during high-risk periods, and practice good field management.",
    "Rice___Neck_Blast": "Plant resistant varieties, improve nutrient management, and apply fungicides if symptoms appear.",
    "Wheat___Brown_Rust": "Apply fungicides and practice crop rotation with non-host crops.",
    "Wheat___Healthy": "Continue with good management practices, including proper fertilization and weed control.",
    "Wheat___Yellow_Rust": "Use resistant varieties, apply fungicides, and rotate crops.",
    "Sugarcane__Red_Rot": "Plant resistant varieties and ensure good drainage.",
    "Sugarcane__Healthy": "Maintain healthy soil conditions and proper irrigation.",
    "Sugarcane__Bacterial Blight": "Use disease-free planting material, practice crop rotation, and destroy infected plants."
}

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
            predicted_class_index = np.argmax(predictions)
            predicted_class = class_labels[predicted_class_index]
            
            # Check if the predicted class is among the known classes
            if predicted_class in solutions:
                solution = solutions[predicted_class]
                return render_template('index.html', predicted_class=predicted_class, solution=solution)
            else:
                # Ask user for the name of the plant/disease
                return render_template('index.html', unknown=True, img_path=img_path)
    @app.route('/submit_unknown', methods=['POST'])
def submit_unknown():
    plant_name = request.form['plant_name']
    img_path = request.form['img_path']
    # You can save or process the unknown plant name as needed
    return render_template('index.html', plant_name=plant_name, img_path=img_path)

if __name__ == '__main__':
    app.run(debug=True)
