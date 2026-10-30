# Steel Surface Inspection

A minimal **English-language web application** for classifying steel surface defects using the trained ResidualSteelCNN from `steel_defect.ipynb`. It keeps the original dark teal template, with only image upload and results: the detected defect, six relative class scores, and one short recommendation.

## Setup on Windows

1. Copy your own trained `steel_residual_best.pth` file into `models/steel_residual_best.pth`. This file is **not included**. It must come from your Jupyter training run (not the notebook itself).
2. Open a terminal in this `steelvision_app` directory and run:

```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 -m uvicorn main:app --reload
```

3. Open **http://127.0.0.1:8000**. Choose or drag a photo. Analysis begins automatically—no questions or submit button.
4. To stop the server, press `Ctrl+C` in the terminal. With `--reload`, edited frontend files appear after a browser refresh (`Ctrl+F5` if cached).

## Files

- `main.py`: FastAPI server, upload validation, short per-class recommendations.
- `model.py`: trained CNN architecture and image preprocessing as used in the notebook (grayscale, 128 × 128).
- `static/index.html`, `static/style.css`, `static/app.js`: English frontend and automatic upload workflow.
- `models/`: location for **your** model weights.

## What scores mean

- Classification covers **six defect types**: Crazing, Inclusion, Pitted Surface, Patches, Rolled-in Scale and Scratches.
- The six displayed percentages are **Softmax class scores** (relative model output). They are **not percentages of surface area, damage severity, or certified probabilities**.
- The brief recommendation is fixed guidance tied to the predicted type. **There is no image-based severity assessment** because NEU-CLS does not have severity labels, damage measurements, or a no-defect class.
- The CNN may label intact or unrelated photos as one of the six defects. Human review is necessary for quality and safety decisions. Real-factory performance has not been established.

## API

- `GET /api/health`: server-side model readiness.
- `POST /api/inspect`: accepts only one multipart field: `file`. Returns English defect name, six class scores and a recommendation.
- `GET /docs`: Swagger docs for developers (not shown to the end user).

No retraining or new dataset downloads are needed for this UI update. The model file remains essential.
