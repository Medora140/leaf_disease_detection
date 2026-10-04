# UrbanLeaf AI: Folder Structure Documentation

```text
plant-disease-backend/
│
├── .gitignore                         # Git exclusion rules (venv, models, temp files)
├── README.md                          # Project overview and quickstart guide
├── requirements.txt                   # Python environment dependencies
├── app_ui.py                          # Streamlit frontend web application
│
├── app/                               # FastAPI backend application module
│   ├── __init__.py                    # Module initializer
│   ├── main.py                        # FastAPI routes and endpoint definitions
│   ├── inference.py                   # ONNX Runtime loader & preprocessing logic
│   └── knowledge_base.py              # Agronomic advice & disease taxonomy mapping
│
├── models/                            # Trained model artifacts
│   ├── resnet18_plantvillage.onnx     # Primary ONNX inference model
│   └── resnet18_best.pth              # PyTorch checkpoint (backup)
│
└── docs/                              # Project technical documentation
    ├── ARCHITECTURE.md                # System architecture & stack specs
    ├── FOLDER_STRUCTURE.md            # Directory layout specification
    ├── DATASET_MANIFEST.md            # Class taxonomy, dataset stats, and split rules
    └── WORKFLOW_KNOWLEDGE.md          # End-to-end development workflow & advice database


---

### File 3: `docs/DATASET_MANIFEST.md`

```markdown
# UrbanLeaf AI: Dataset Manifest & Class Taxonomy

## Canonical Taxonomy (10 Classes)
UrbanLeaf AI focuses on 3 primary urban container crops (Pepper, Potato, Tomato) alongside an Out-Of-Distribution (`background_other`) rejection class.

| Class ID | Canonical Class Name | Target Crop | Condition |
| :---: | :--- | :--- | :--- |
| 0 | `background_other` | Non-Crop / OOD | Rejection Class |
| 1 | `pepper_bacterial_spot` | Bell Pepper | Bacterial Spot (*Xanthomonas spp.*) |
| 2 | `pepper_healthy` | Bell Pepper | Healthy |
| 3 | `potato_early_blight` | Potato | Early Blight (*Alternaria solani*) |
| 4 | `potato_healthy` | Potato | Healthy |
| 5 | `potato_late_blight` | Potato | Late Blight (*Phytophthora infestans*) |
| 6 | `tomato_early_blight` | Tomato | Early Blight (*Alternaria solani*) |
| 7 | `tomato_healthy` | Tomato | Healthy |
| 8 | `tomato_late_blight` | Tomato | Late Blight (*Phytophthora infestans*) |
| 9 | `tomato_septoria_leaf_spot` | Tomato | Septoria Leaf Spot (*Septoria lycopersici*) |

---

## Dataset Distribution & Stratified Split

Total Processed Images: **12,025**  
Deduplication Strategy: Perceptual Difference Hashing ($dHash$) — 0 redundant duplicates found.

| Class Name | Train (80%) | Val (10%) | Test (10%) | Total Count |
| :--- | :---: | :---: | :---: | :---: |
| `background_other` | 913 | 114 | 114 | 1,141 |
| `pepper_bacterial_spot` | 798 | 99 | 100 | 997 |
| `pepper_healthy` | 1,182 | 148 | 148 | 1,478 |
| `potato_early_blight` | 800 | 100 | 100 | 1,000 |
| `potato_healthy` | 121 | 16 | 15 | 152 |
| `potato_late_blight` | 800 | 100 | 100 | 1,000 |
| `tomato_early_blight` | 800 | 100 | 100 | 1,000 |
| `tomato_healthy` | 1,268 | 158 | 159 | 1,585 |
| `tomato_late_blight` | 1,521 | 190 | 190 | 1,901 |
| `tomato_septoria_leaf_spot` | 1,417 | 177 | 177 | 1,771 |
| **TOTAL** | **9,620** | **1,202** | **1,203** | **12,025** |

---

## Baseline ResNet-18 Metrics
- **Validation Accuracy:** 99.67%
- **Test Accuracy:** 99.92%
- **Test Set Loss:** 0.0137