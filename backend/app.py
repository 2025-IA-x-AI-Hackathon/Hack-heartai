from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
import pandas as pd
import io

app = FastAPI(title="Hack-heartai API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "up"}

# --- 스키마 ---
class PredictRow(BaseModel):
    sepal_length: float = Field(..., example=5.1)
    sepal_width:  float = Field(..., example=3.5)
    petal_length: float = Field(..., example=1.4)
    petal_width:  float = Field(..., example=0.2)

class PredictReq(BaseModel):
    rows: list[PredictRow]

# --- 예측(Mock) ---
@app.post("/predict")
def predict(req: PredictReq):
    df = pd.DataFrame([r.model_dump() for r in req.rows])
    df["prediction"] = 0  # <- 모델 오면 교체
    return {
        "columns": list(df.columns),
        "rows": df.to_dict(orient="records"),
        "count": len(df)
    }
