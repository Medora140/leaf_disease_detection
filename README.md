# UrbanLeaf AI — Plant Disease Detection

UrbanLeaf AI is a small web application for checking photos of pepper, potato, and tomato leaves. It classifies an image into one of ten supported health categories and returns concise care and prevention notes for the predicted category. The project combines a Streamlit interface, a FastAPI service, image preprocessing, and a ResNet-18 model exported to ONNX.

> The result is an image classification aid, not a confirmed diagnosis. The model only covers the categories listed below and may be unreliable on images unlike its training data.

## Features

- Upload JPG, JPEG, or PNG leaf images in the Streamlit interface.
- Optionally isolate the largest detected object with YOLOv8 segmentation before classification; if no mask is detected, inference continues with the original image.
- Run ResNet-18 classification through ONNX Runtime and display the predicted class and confidence.
- Return symptoms, immediate-action, and prevention notes mapped to the predicted class.
- Browse a simple results page and use the built-in keyword-based care helper, which selects from the same local guidance notes.
- Expose inference through a FastAPI `POST /predict` endpoint.

### Supported categories

| Crop | Categories |
| --- | --- |
| Background / other | `background_other` |
| Pepper | `pepper_bacterial_spot`, `pepper_healthy` |
| Potato | `potato_early_blight`, `potato_healthy`, `potato_late_blight` |
| Tomato | `tomato_early_blight`, `tomato_healthy`, `tomato_late_blight`, `tomato_septoria_leaf_spot` |

## Architecture

```text
User selects image
       |
       v
Streamlit UI (app_ui.py) -- HTTP POST /predict --> FastAPI (app/main.py)
                                                       |
                                                       v
                                            DiseasePredictor (app/inference.py)
                                             |                 |
                                      YOLOv8 segmentation   Image preprocessing
                                                               |
                                                               v
                                                    ONNX Runtime / ResNet-18
                                                               |
                                                               v
                                          class + confidence + knowledge-base advice
                                                               |
                                                               v
                                                     JSON response to UI
```

1. The Streamlit UI sends the uploaded image bytes to the local API.
2. FastAPI validates that the upload is an image and calls `DiseasePredictor`.
3. The predictor uses YOLOv8 segmentation to isolate the largest detected object where possible. It then resizes the image to 256 × 256, applies ImageNet mean/std normalization, and rearranges it into the model's NCHW input format.
4. ONNX Runtime runs the ResNet-18 classifier. The code applies softmax to the output scores and selects the highest-probability class.
5. The API adds the matching guidance from `app/knowledge_base.py` and returns the result as JSON. The UI displays the prediction, confidence, and care notes.

The ONNX model and its external tensor data are stored in `models/`. The class index order used at inference is defined in `app/inference.py`; `data/class_mappings.json` is a companion class mapping artifact.

## Languages and technologies

- **Python** — API, UI, inference, and guidance logic.
- **Markdown** — project and technical documentation.
- **JSON** — class mapping data and notebook file format.
- **CSV** — metadata artifact (`data/metadata.csv`).
- **HTML/CSS** — UI markup and styling embedded in the Python Streamlit app.
- **Jupyter notebooks** — five notebook files are present under `notebooks/`, but they are empty in this checkout.

Core libraries include FastAPI, Uvicorn, Streamlit, Requests, ONNX Runtime, NumPy, OpenCV, Pillow, Pydantic, and Ultralytics YOLO. `requirements.txt` lists the main runtime packages but currently does **not** list `ultralytics`, which `app/inference.py` imports. Install it separately as shown below.

## Requirements

- Python 3.10 or newer is recommended.
- Install dependencies from `requirements.txt` and install Ultralytics separately.
- The ONNX model files `models/resnet18_plantvillage.onnx` and `models/resnet18_plantvillage.onnx.data` must be present.
- YOLOv8 segmentation weights are loaded from `yolov8n-seg.pt`. A file with that name is present in some checkouts; if it is not available locally, Ultralytics may need network access to obtain the weights.

## Run locally

Run these commands from the repository root. Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install ultralytics
```

Start the API in one terminal:

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Start the Streamlit app in a second terminal, with the same virtual environment activated:

```powershell
streamlit run app_ui.py
```

Open the local URL printed by Streamlit. The UI is configured to call `http://127.0.0.1:8000/predict`, so the API must be running on that address and port. The API's interactive documentation is available at `http://127.0.0.1:8000/docs`.

### API quick reference

- `GET /` — returns a simple API liveness message.
- `POST /predict` — multipart form upload with an image field named `file`.

A successful prediction response includes `success`, the uploaded filename, and a `data` object containing `prediction`, `confidence` (percentage), `class_id`, and `agricultural_guidance`.

## Repository layout

```text
.
├── app/
│   ├── main.py                 # FastAPI endpoints
│   ├── inference.py            # Segmentation, preprocessing, ONNX inference
│   └── knowledge_base.py       # Class-specific advice
├── app_ui.py                   # Streamlit user interface
├── data/
│   ├── class_mappings.json     # Class mapping data
│   └── metadata.csv            # Metadata artifact
├── docs/                       # Architecture, dataset, folder, and workflow notes
├── models/                     # ONNX model and external tensor data
├── notebooks/                  # Named workflow notebooks (empty in this checkout)
├── requirements.txt            # Main Python dependencies
└── yolov8n-seg.pt              # YOLOv8 segmentation weights, when supplied locally
```

## Motive

The project aims to make an initial plant-health check accessible to home and urban growers. A user can submit a leaf photo, get a model-generated category, and see practical next-step information in one place. The supported scope is deliberately limited to three crops and the classes represented by the supplied classifier.

## Advantages

- A local web UI and API make the inference flow straightforward to run and integrate.
- ONNX Runtime provides a framework-independent format for serving the classifier.
- The preprocessing pipeline attempts to reduce background clutter through segmentation and has a fallback when segmentation returns no mask.
- The result combines a confidence value with understandable, class-specific symptom and care notes.
- The code is divided into UI, API, inference, and knowledge-base modules.

## Disadvantages and limitations

- The classifier recognizes only the ten listed classes; it does not cover all crops, pests, nutrient problems, or diseases.
- Predictions depend on the training data and image quality. Confidence is a model score, not a guarantee of correctness or calibrated certainty.
- YOLO segmentation selects the largest detected mask as the leaf, but the code does not verify that the detected object is actually a leaf. Background segmentation or tight cropping can affect classification.
- The Streamlit helper is keyword-based and returns fixed notes; it is not a conversational language model and does not provide free-form agronomic reasoning.
- The advice is static and should be checked against local agricultural guidance and product labels.
- The API currently permits all CORS origins and has no authentication, rate limiting, or production deployment configuration.
- `ultralytics` is imported by the inference module but is missing from `requirements.txt`; setup therefore requires an extra install. YOLO weights may also require a separate local file or network download.
- The checked-in notebook files are zero bytes, so training, evaluation, Grad-CAM, and data-cleaning workflows described in documentation are not runnable from those notebooks in this checkout.

## Project documentation

- `docs/Architecture.md` — architecture and model design notes.
- `docs/Dataset.md` — dataset references.
- `docs/Folder.md` — folder-structure notes.
- `docs/workflow_knowledge.md` — intended development workflow and guidance notes.
