from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import time
import json
from joblib import load
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Iris Classifier API", version="1.0.0")
Instrumentator().instrument(app).expose(app)

origins = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")
MODEL_META_PATH = os.path.join(MODEL_DIR, "model_metadata.json")

_model = None
_model_meta: dict = {}

def load_model() -> bool:
    global _model, _model_meta
    try:
        _model = load(MODEL_PATH)
        if os.path.exists(MODEL_META_PATH):
            with open(MODEL_META_PATH, "r") as f:
                _model_meta = json.load(f)
        else:
            _model_meta = {}
        print("[INFO] Model loaded:", True)
        return True
    except Exception as e:
        print(f"[WARN] Could not load model: {e}")
        _model = None
        _model_meta = {}
        return False

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictRequest(BaseModel):
    items: List[IrisInput]

class PredictResponse(BaseModel):
    predictions: List[int]
    predicted_names: Optional[List[str]] = None
    classes: Optional[List[str]] = None
    model: Optional[dict] = None
    latency_ms: Optional[float] = None
    probabilities: Optional[List[List[float]]] = None

@app.on_event("startup")
def on_startup():
    load_model()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": _model is not None,
        "model_meta": _model_meta,
    }

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Add app/model/model.joblib and rebuild the API.",
        )

    X = [
        [
            it.sepal_length,
            it.sepal_width,
            it.petal_length,
            it.petal_width,
        ]
        for it in req.items
    ]

    start = time.time()
    y = _model.predict(X).tolist()
    latency_ms = (time.time() - start) * 1000.0

    class_ids = list(getattr(_model, "classes_", []))

    target_names = []
    if isinstance(_model_meta, dict):
        tn = _model_meta.get("target_names")
        if isinstance(tn, list) and all(isinstance(x, str) for x in tn):
            target_names = tn

    if not target_names and class_ids:
        target_names = [str(c) for c in class_ids]

    def id_to_name(cid: int) -> str:
        try:
            return target_names[int(cid)]
        except Exception:
            return str(cid)

    predicted_names = [id_to_name(p) for p in y]

    probs = None
    if hasattr(_model, "predict_proba"):
        try:
            probs = _model.predict_proba(X).tolist()
        except Exception as e:
            print(f"[WARN] predict_proba failed: {e}")

    classes_readable = target_names if target_names else [str(c) for c in class_ids]

    return PredictResponse(
        predictions=y,
        predicted_names=predicted_names,
        classes=classes_readable,
        model=_model_meta,
        latency_ms=latency_ms,
        probabilities=probs,
    )
