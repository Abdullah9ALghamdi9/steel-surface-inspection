"""Steel Surface Inspection — run with: py -3.13 -m uvicorn main:app --reload"""
from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageOps, UnidentifiedImageError

from model import SteelPredictor

ROOT = Path(__file__).resolve().parent
WEIGHTS_PATH = ROOT / "models" / "steel_residual_best.pth"
MAX_BYTES = 10 * 1024 * 1024
MAX_PIXELS = 20_000_000
ALLOWED_FORMATS = {"PNG", "JPEG", "BMP", "WEBP"}

# General visual-inspection advice; these do not infer severity or area of damage.
RECOMMENDATIONS = {
    "Cr": "Inspect the affected area to check how far the cracks extend.",
    "In": "Check the affected area for embedded material and surface irregularities.",
    "PS": "Inspect the pitted area and measure its extent before acceptance.",
    "Pa": "Review the affected patch during routine quality inspection.",
    "RS": "Inspect the scale marks and assess whether surface rework is needed.",
    "Sc": "Check scratch depth before deciding on polishing or rework.",
}

predictor = SteelPredictor(WEIGHTS_PATH)
app = FastAPI(title="Steel Surface Inspection", version="2.0.0", description="Image-based classification of six steel surface defect types")
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")


@app.get("/")
def homepage():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/api/health")
def health():
    if not predictor.ready and WEIGHTS_PATH.is_file():
        predictor.load()
    return {"model_ready": predictor.ready, "detail": "Ready" if predictor.ready else predictor.load_error}


@app.post("/api/inspect")
async def inspect(file: UploadFile = File(...)):
    if not predictor.ready:
        if WEIGHTS_PATH.is_file():
            predictor.load()
        if not predictor.ready:
            raise HTTPException(status_code=503, detail=predictor.load_error or "Model weights are not available.")

    raw = await file.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image exceeds the 10 MB limit.")
    if not raw:
        raise HTTPException(status_code=400, detail="Please upload an image.")

    try:
        with Image.open(BytesIO(raw)) as image:
            if image.format not in ALLOWED_FORMATS:
                raise HTTPException(status_code=415, detail="Unsupported image format. Use PNG, JPG, BMP, or WEBP.")
            if image.width * image.height > MAX_PIXELS:
                raise HTTPException(status_code=413, detail="Image dimensions are too large.")
            image.load()
            image = ImageOps.exif_transpose(image).copy()
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        raise HTTPException(status_code=400, detail="The image could not be read.")

    prediction = predictor.predict(image)
    return {
        "prediction": prediction,
        "recommendation": RECOMMENDATIONS[prediction["defect_code"]],
    }
