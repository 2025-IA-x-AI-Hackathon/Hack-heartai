# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path
# Input data files are available in the read-only "../input/" director
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

df = pd.read_csv('mental_health_wearable_data.csv')

print(df.head(3))
print(df.info())
print(df.isnull().sum())

y = df['Mental_Health_Condition']
x = df.drop('Mental_Health_Condition',axis=1)

x_train,x_test,y_train,y_test = train_test_split(x,y,train_size=0.78,random_state=45)

lr = LogisticRegression()
model = lr.fit(x_train,y_train)
print(f"\n모델 정확도: {model.score(x_test,y_test):.4f}")

# Feature Importance 분석 (Logistic Regression 계수)
print("\n" + "="*60)
print("Feature Importance 분석")
print("="*60)

# 계수 추출
coefficients = model.coef_[0]
feature_names = x.columns

# Feature importance DataFrame 생성
feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': coefficients,
    'Abs_Coefficient': np.abs(coefficients),
    'Impact': ['양의 영향' if coef > 0 else '음의 영향' for coef in coefficients]
})

# 절대값 기준으로 정렬 (영향도가 큰 순서대로)
feature_importance_df = feature_importance_df.sort_values('Abs_Coefficient', ascending=False)

# 상위 영향도 Feature 출력
print("\n[Feature별 영향도 순위 (절대값 기준)]")
print("-"*60)
for idx, row in feature_importance_df.iterrows():
    print(f"{row['Feature']:30s}: {row['Coefficient']:10.4f} ({row['Impact']})")

print("\n[상세 분석 표]")
print(feature_importance_df.to_string(index=False))

# 영향도 요약
print("\n[영향도 요약]")
print("-"*60)
print(f"가장 영향이 큰 Feature: {feature_importance_df.iloc[0]['Feature']}")
print(f"  - 계수 값: {feature_importance_df.iloc[0]['Coefficient']:.4f}")
print(f"  - 영향: {feature_importance_df.iloc[0]['Impact']}")

if len(feature_importance_df) > 1:
    print(f"\n두 번째로 영향이 큰 Feature: {feature_importance_df.iloc[1]['Feature']}")
    print(f"  - 계수 값: {feature_importance_df.iloc[1]['Coefficient']:.4f}")
    print(f"  - 영향: {feature_importance_df.iloc[1]['Impact']}")

# CSV 파일로 저장 (보고서용)
save_dir = Path(__file__).parent  # 현재 train_model.py가 있는 폴더(model/)
csv_path = save_dir / 'feature_importance_report.csv'
try:
    feature_importance_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print("\n[보고서 파일 저장 완료]")
    print(f"feature_importance_report.csv 파일이 생성되었습니다: {csv_path}")
except PermissionError as e:
    print(f"\n[⚠️ 경고] 파일 저장 실패 (파일이 다른 프로그램에서 열려있을 수 있습니다)")
    print(f"파일 경로: {csv_path}")
    print(f"에러: {e}")
    print("해결 방법: Excel이나 다른 프로그램에서 해당 CSV 파일을 닫고 다시 시도하세요.")

# ====================================================================
# 개별 인스턴스 예측 기여도 분석
# ====================================================================
print("\n" + "="*60)
print("개별 인스턴스 예측 기여도 분석")
print("="*60)

def calculate_individual_feature_contribution(model, instance, feature_names):
    """
    개별 인스턴스에 대한 각 feature의 기여도를 계산
    Logistic Regression의 경우: 기여도 = feature_value * coefficient
    """
    instance_array = instance.values if hasattr(instance, 'values') else instance
    coefficients = model.coef_[0]
    intercept = model.intercept_[0]
    
    # 각 feature의 기여도 계산 (로지스틱 회귀의 선형 조합 부분)
    contributions = instance_array * coefficients
    
    # 예측 확률 계산
    linear_combination = np.sum(contributions) + intercept
    probability = 1 / (1 + np.exp(-linear_combination))
    
    # 기여도 DataFrame 생성
    contribution_df = pd.DataFrame({
        'Feature': feature_names,
        'Feature_Value': instance_array,
        'Coefficient': coefficients,
        'Contribution': contributions,
        'Abs_Contribution': np.abs(contributions),
        'Impact': ['증가시키는 방향' if c > 0 else '감소시키는 방향' for c in contributions]
    })
    
    # 절대값 기준 정렬
    contribution_df = contribution_df.sort_values('Abs_Contribution', ascending=False)
    
    return contribution_df, probability, linear_combination

# 테스트 데이터에서 몇 개 샘플 선택하여 분석
print("\n[샘플 개인별 예측 기여도 분석]")
print("-"*60)

# 테스트 데이터에서 몇 개 샘플 선택 (예: 처음 3개)
sample_indices = x_test.index[:3]

for idx in sample_indices:
    instance = x_test.loc[[idx]].iloc[0]
    actual_label = y_test.loc[idx]
    
    # 예측 수행
    prediction = model.predict([instance])[0]
    prediction_proba = model.predict_proba([instance])[0]
    
    # Feature 기여도 계산
    contribution_df, prob, linear_comb = calculate_individual_feature_contribution(
        model, instance, x.columns
    )
    
    print(f"\n[개인 ID: {idx}]")
    print(f"실제 Mental_Health_Condition: {actual_label}")
    print(f"예측 Mental_Health_Condition: {prediction}")
    print(f"예측 확률 (1일 가능성): {prediction_proba[1]:.4f}")
    print(f"\n각 Feature의 기여도:")
    print("-"*60)
    
    for _, row in contribution_df.iterrows():
        print(f"{row['Feature']:30s}: 값={row['Feature_Value']:8.2f}, "
              f"기여도={row['Contribution']:8.4f} ({row['Impact']})")
    
    # 가장 영향이 큰 feature 표시
    top_feature = contribution_df.iloc[0]
    print(f"\n→ 가장 영향이 큰 Feature: {top_feature['Feature']}")
    print(f"  - 기여도: {top_feature['Contribution']:.4f}")
    print(f"  - 이 개인의 {top_feature['Feature']} 값: {top_feature['Feature_Value']:.2f}")
    
    # CSV 파일로 저장
    contribution_df['Individual_ID'] = idx
    contribution_df['Actual_Label'] = actual_label
    contribution_df['Predicted_Label'] = prediction
    contribution_df['Prediction_Probability'] = prediction_proba[1]
    
    output_file = save_dir / f'individual_contribution_{idx}.csv'
    try:
        contribution_df[['Individual_ID', 'Feature', 'Feature_Value', 'Coefficient', 
                         'Contribution', 'Abs_Contribution', 'Impact', 
                         'Actual_Label', 'Predicted_Label', 'Prediction_Probability']].to_csv(
            output_file, index=False, encoding='utf-8-sig')
        print(f"  → {output_file.name} 파일로 저장됨")
    except PermissionError as e:
        print(f"  → ⚠️ {output_file.name} 파일 저장 실패 (파일이 Excel이나 다른 프로그램에서 열려있을 수 있습니다)")
        print(f"     파일 경로: {output_file}")
        print(f"     해결 방법: 해당 CSV 파일을 닫고 다시 시도하세요.")

print("\n" + "="*60)
print("개별 인스턴스 분석 완료")
print("="*60)

# 특정 인스턴스 분석 함수 (재사용 가능)
def analyze_individual(model, features_dict, feature_names):
    """
    특정 개인의 데이터를 입력받아 예측 기여도 분석
    
    사용 예:
    features_dict = {
        'Heart_Rate_BPM': 95,
        'Sleep_Duration_Hours': 7.5,
        'Physical_Activity_Steps': 12000,
        'Mood_Rating': 6
    }
    result_df, prob, pred = analyze_individual(model, features_dict, x.columns)
    """
    # 딕셔너리를 DataFrame으로 변환
    instance_df = pd.DataFrame([features_dict])
    instance = instance_df.iloc[0]
    
    prediction = model.predict([instance])[0]
    prediction_proba = model.predict_proba([instance])[0]
    
    contribution_df, prob, linear_comb = calculate_individual_feature_contribution(
        model, instance, feature_names
    )
    
    return contribution_df, prediction_proba[1], prediction

print("\n[사용법 안내]")
print("-"*60)
print("특정 개인의 데이터를 분석하려면 다음과 같이 사용하세요:")
print("""
from train_model_new_data import analyze_individual

# 개인 데이터 입력
개인_데이터 = {
    'Heart_Rate_BPM': 95,
    'Sleep_Duration_Hours': 7.5,
    'Physical_Activity_Steps': 12000,
    'Mood_Rating': 6
}

# 분석 실행
기여도_df, 확률, 예측 = analyze_individual(model, 개인_데이터, x.columns)
print(기여도_df)
""")

# 모델 저장 (이미 save_dir은 위에서 정의됨)
model_path = save_dir / "model.joblib"
feature_path = save_dir / "feature_order.joblib"

try:
    joblib.dump(model, model_path)
    joblib.dump(list(x.columns), feature_path)
    print(f"\n[✅ 모델 저장 완료]")
    print(f" - model: {model_path.resolve()}")
    print(f" - feature_order: {feature_path.resolve()}")
except PermissionError as e:
    print(f"\n[⚠️ 경고] 모델 저장 실패 (파일이 다른 프로그램에서 열려있을 수 있습니다)")
    print(f"파일 경로: {model_path} 또는 {feature_path}")
    print(f"에러: {e}")
    print("해결 방법: 해당 파일을 사용하는 프로그램을 종료하고 다시 시도하세요.")