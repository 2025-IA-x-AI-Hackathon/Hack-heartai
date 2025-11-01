# train_and_save.py
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("mental_health_wearable_data.csv")

y = df["Mental_Health_Condition"]
X = df.drop(columns=["Mental_Health_Condition"])

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.78, random_state=45)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print(f"Accuracy: {model.score(X_test, y_test):.4f}")

# 배포용 아티팩트 저장
joblib.dump(model, "model.joblib")
joblib.dump(list(X.columns), "feature_order.joblib")  # ['Heart_Rate_BPM', 'Sleep_Duration_Hours', ...]
print("saved: model.joblib, feature_order.joblib")
