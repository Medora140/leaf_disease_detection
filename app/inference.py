import io
import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image

# Class index mapping (exact match with trained ResNet-18)
CLASS_NAMES = [
    "background_other",
    "pepper_bacterial_spot",
    "pepper_healthy",
    "potato_early_blight",
    "potato_healthy",
    "potato_late_blight",
    "tomato_early_blight",
    "tomato_healthy",
    "tomato_late_blight",
    "tomato_septoria_leaf_spot"
]

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD  = np.array([0.229, 0.224, 0.225], dtype=np.float32)

class DiseasePredictor:
    def __init__(self, model_path: str):
        # Initialize ONNX session
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        # Decode image bytes to RGB NumPy array
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_np = np.array(pil_img)
        
        # Resize to 256x256
        img_resized = cv2.resize(img_np, (256, 256))
        
        # Normalize and reorder dimensions: (H, W, C) -> (1, C, H, W)
        input_data = img_resized.astype(np.float32) / 255.0
        input_data = (input_data - MEAN) / STD
        input_data = np.transpose(input_data, (2, 0, 1))
        input_data = np.expand_dims(input_data, axis=0)
        
        return input_data

    def predict(self, image_bytes: bytes):
        input_tensor = self.preprocess_image(image_bytes)
        
        # Run ONNX inference
        outputs = self.session.run(None, {self.input_name: input_tensor})[0]
        
        # Compute Softmax probabilities
        exp_scores = np.exp(outputs - np.max(outputs))
        probabilities = exp_scores / np.sum(exp_scores)
        
        pred_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[0][pred_idx])
        pred_class = CLASS_NAMES[pred_idx]
        
        return {
            "prediction": pred_class,
            "confidence": round(confidence * 100, 2),
            "class_id": pred_idx
        }