# UrbanLeaf AI: System Architecture Document

## Overview
UrbanLeaf AI is a production-grade, modular deep-learning computer vision system designed for urban plant disease detection, spatial localization, severity estimation, and automated agronomic guidance.

---

## Technical Stack
- **Frontend UI:** Streamlit (`app_ui.py`)
- **Backend API:** FastAPI (`app/main.py`)
- **Inference Engine:** ONNX Runtime (`onnxruntime`)
- **Deep Learning Framework:** PyTorch & Torchvision (Training & Export)
- **Computer Vision & Augmentation:** OpenCV, Albumentations, PyTorch-Grad-CAM
- **Data Engineering:** Pandas, ImageHash (Deduplication)

---

## Pipeline Architecture

[ User Image Input ]
                                     │
                                     ▼
                         [ Streamlit Web UI ]
                                     │
                              (HTTP POST /predict)
                                     │
                                     ▼
                         [ FastAPI Server ]
                                     │
                                     ▼
                 ┌───────────────────────────────────────┐
                 │          Image Preprocessing          │
                 │  - Resize to 256x256                   │
                 │  - ImageNet Normalization (Mean/Std)   │
                 │  - Reorder Dimensions to (1, 3, H, W)  │
                 └───────────────────┬───────────────────┘
                                     │
                                     ▼
                 ┌───────────────────────────────────────┐
                 │          ONNX Runtime Engine          │
                 │  - Model: ResNet-18 (10 Classes)     │
                 │  - Softmax Probability Computation   │
                 └───────────────────┬───────────────────┘
                                     │
                                     ▼
                 ┌───────────────────────────────────────┐
                 │      Agronomic Knowledge Mapping      │
                 │  - Class Label to Guidance Mapping    │
                 │  - Symptoms, Containment, Prevention  │
                 └───────────────────┬───────────────────┘
                                     │
                                     ▼
                         [ JSON Response Payload ]
                                     │
                                     ▼
                         [ Streamlit UI Render ]
           (Diagnosis, Confidence %, Symptoms, Containment, Prevention)

---

## Deep Learning Specifications
- **Base Model:** ResNet-18 (Pre-trained on ImageNet)
- **Custom Classification Head:** Linear Layer with Dropout ($p=0.3$), output shape = 10 classes.
- **Input Resolution:** $256 \times 256 \times 3$
- **Optimization Strategy:** AdamW ($\text{lr}=10^{-3}$, $\text{weight\_decay}=10^{-4}$) with Cosine Annealing Learning Rate Scheduler.
- **Explainability:** Grad-CAM / Grad-CAM++ targeting deep feature maps (`layer3` and `layer4`) for lesion localization.