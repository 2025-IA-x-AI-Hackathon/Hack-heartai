# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Annotated
from pathlib import Path
import os

import numpy as np 
import joblib

app = FastAPI(title="Stress Risk 7-Day API", version="1.0.0")

# CORS
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 아티팩트 로드 (루트/model/...) =====
ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "model" / "model.joblib"
FEATURE_PATH = ROOT / "model" / "feature_order.joblib"

try:
    model = joblib.load(MODEL_PATH)
    feature_order: list[str] = joblib.load(FEATURE_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load artifacts: {e}")

# ===== 스키마 =====
class DaySample(BaseModel):
    Heart_Rate_BPM: float = Field(..., description="심박수 BPM")
    Sleep_Duration_Hours: float = Field(..., description="수면 시간(시간)")
    Physical_Activity_Steps: float = Field(..., description="일일 걸음 수")
    Mood_Rating: float = Field(..., ge=1, le=10, description="오늘의 기분(1~10)")

# 정확히 7일치 제한
Days7 = Annotated[List[DaySample], Field(min_items=7, max_items=7)]

class Predict7Request(BaseModel):
    days: Days7
    threshold: float = Field(0.5, ge=0.0, le=1.0)

class Predict7ResponseItem(BaseModel):
    day: int
    prob: float
    label: int

class Predict7Response(BaseModel):
    results: List[Predict7ResponseItem]

# ===== 유틸 =====
def to_matrix(days: List[DaySample]) -> np.ndarray:
    rows = []
    for d in days:
        rows.append([getattr(d, col) for col in feature_order])
    return np.array(rows, dtype=float)

@app.get("/")
def health():
    return {"ok": True, "service": "Stress Risk 7-Day API"}

@app.post("/predict7", response_model=Predict7Response)
def predict7(payload: Predict7Request):
    if len(payload.days) != 7:
        raise HTTPException(400, "days must contain exactly 7 items")

    X = to_matrix(payload.days)

    try:
        proba = model.predict_proba(X)[:, 1]
    except AttributeError:
        preds = model.predict(X)
        proba = preds.astype(float)

    labels = (proba >= payload.threshold).astype(int)
    results = [
        {"day": i + 1, "prob": float(p), "label": int(l)}
        for i, (p, l) in enumerate(zip(proba, labels))
    ]
    return {"results": results}
