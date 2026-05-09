import os
import uuid
import shutil
from flask import Blueprint, request, jsonify
from backend.services.inference import predict_image

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    os.makedirs("temp", exist_ok=True)
    path = os.path.join("temp", uuid.uuid4().hex + ".jpg")
    try:
        file.save(path)
        result = predict_image(path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.isfile(path):
            os.remove(path)
