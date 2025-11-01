from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os, hashlib
import numpy as np

app = FastAPI(title="Score API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOW_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatrixInput(BaseModel):
    matrix: List[List[float]]  # 28xF

@app.post("/predict")
def predict(payload: MatrixInput):
    X = np.array(payload.matrix, dtype=float)
    if X.ndim != 2 or X.shape[0] != 28:
        raise HTTPException(400, "matrix must have shape [28, F]")
    # 임시 스코어(입력 해시 기반 0~63): 모델 나오면 교체
    h = hashlib.sha256(X.tobytes()).hexdigest()
    score = int(h[:4], 16) % 64
    return {"score": score}
