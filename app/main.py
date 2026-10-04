import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.inference import DiseasePredictor
from app.knowledge_base import get_disease_advice

app = FastAPI(
    title="Plant Disease Detection API",
    description="ONNX Runtime powered inference API for PlantVillage dataset",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join("models", "resnet18_plantvillage.onnx")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"ONNX model file not found at: {MODEL_PATH}")

predictor = DiseasePredictor(model_path=MODEL_PATH)

@app.get("/")
def read_root():
    return {"message": "Plant Disease Detection API is live!"}

@app.post("/predict")
async def predict_leaf_disease(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        contents = await file.read()
        prediction_res = predictor.predict(contents)
        
        # Attach treatment & prevention guidance
        advice = get_disease_advice(prediction_res["prediction"])
        prediction_res["agricultural_guidance"] = advice

        return {
            "success": True,
            "filename": file.filename,
            "data": prediction_res
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")