# UrbanLeaf AI: Project Workflow & Agronomic Knowledge Base

## End-to-End Execution Workflow

### Phase 1: Data Engineering & Validation (Colab)
1. Selective extraction of target crop categories from PlantVillage and PlantDoc datasets.
2. Deduplication check using perceptual hashing (`imagehash.dhash`).
3. Stratified $80/10/10$ train/val/test splitting saved to `dataset_manifest.csv`.
4. Albumentations transformation pipeline (random flips, rotations, shift-scale-rotate, color jitter).

### Phase 2: Model Benchmarking & Fine-Tuning (Colab)
1. Transfer learning setup with ResNet-18 pretrained on ImageNet.
2. Training using AdamW optimizer and Cosine Annealing scheduler over 10 epochs.
3. Performance evaluation using Confusion Matrix and Classification Metrics (Precision, Recall, F1).

### Phase 3: Model Explainability (Colab)
1. Feature map extraction using Grad-CAM and Grad-CAM++.
2. Visualizing focus regions on `layer3` ($16 \times 16$) and `layer4` ($8 \times 8$) to confirm spatial localization of leaf lesions over background noise.

### Phase 4: Model Export & Serving (VS Code)
1. Exporting PyTorch model to optimized ONNX (`resnet18_plantvillage.onnx`).
2. Verification of ONNX inference session execution via `onnxruntime`.
3. Development of FastAPI backend (`app/main.py`) and Streamlit web dashboard (`app_ui.py`).

---

## Agronomic Guidance Knowledge Base

### 1. Pepper Bacterial Spot (*Xanthomonas spp.*)
- **Symptoms:** Small, water-soaked dark spots on leaves that turn brown with yellow halos, leading to defoliation.
- **Immediate Action:** Prune and destroy infected leaves immediately. Disinfect tools between cuts.
- **Prevention:** Apply copper-based bactericides early in the season; avoid overhead irrigation.

### 2. Potato Early Blight (*Alternaria solani*)
- **Symptoms:** Dark brown/black spots with concentric rings ("target board" pattern) on mature leaves.
- **Immediate Action:** Remove lower affected foliage. Apply approved fungicides like chlorothalonil or mancozeb.
- **Prevention:** Practice a 2–3 year crop rotation; irrigate early in the morning so foliage dries quickly.

### 3. Potato Late Blight (*Phytophthora infestans*)
- **Symptoms:** Large dark green to purplish-black water-soaked lesions that expand rapidly under cool, wet conditions.
- **Immediate Action:** Immediately prune infected stems and dispose in sealed bags (do not compost). Apply systemic copper hydroxide.
- **Prevention:** Plant resistant cultivars, maintain proper hilling, and eliminate volunteer potato plants.

### 4. Tomato Early Blight (*Alternaria solani*)
- **Symptoms:** Concentric ring brown spots appearing on lower leaves, surrounded by yellow chlorotic tissue.
- **Immediate Action:** Strip infected lower leaves up to the first fruit cluster. Apply copper sprays.
- **Prevention:** Mulch soil base to stop fungal spores from splashing up during rain; maintain wide plant spacing.

### 5. Tomato Late Blight (*Phytophthora infestans*)
- **Symptoms:** Irregular dark brown greasy spots with yellow borders; rapid defoliation during high humidity.
- **Immediate Action:** Isolate infected plants. Remove infected branches with disinfected shears.
- **Prevention:** Avoid working in the garden when foliage is wet. Maximize sunlight exposure and air circulation.

### 6. Tomato Septoria Leaf Spot (*Septoria lycopersici*)
- **Symptoms:** Numerous small circular spots with gray-white centers and dark brown margins containing tiny black specks.
- **Immediate Action:** Prune affected leaves near the ground level. Disinfect tools with 70% isopropyl alcohol.
- **Prevention:** Use drip lines instead of overhead sprinklers; cover soil with clean straw mulch.