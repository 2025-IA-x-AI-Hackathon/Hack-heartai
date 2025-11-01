# Hack-heartai

## Mental Health Prediction Model - Feature Importance Analysis

웨어러블 기기 데이터를 기반으로 정신 건강 상태를 예측하는 Logistic Regression 모델입니다.

## 필수 요구사항

```bash
pip install numpy pandas scikit-learn
```

## 📥 입력 (Input)

### 입력 파일: `mental_health_wearable_data.csv`

스크립트와 동일한 디렉토리에 위치해야 합니다.

#### 필수 컬럼

| 컬럼명 | 설명 | 데이터 타입 | 예시 |
|--------|------|------------|------|
| `Heart_Rate_BPM` | 심박수 (분당 비트 수) | Numeric | 98 |
| `Sleep_Duration_Hours` | 수면 시간 (시간) | Numeric | 7.43 |
| `Physical_Activity_Steps` | 신체 활동 걸음 수 | Numeric | 13760 |
| `Mood_Rating` | 기분 평가 점수 | Numeric | 5 |
| `Mental_Health_Condition` | 정신 건강 상태 (타겟 변수) | Binary (0 또는 1) | 1 |

#### 데이터 형식 예시

```csv
Heart_Rate_BPM,Sleep_Duration_Hours,Physical_Activity_Steps,Mood_Rating,Mental_Health_Condition
98,7.425123617672569,13760,5,1
111,9.457572346665666,11455,9,0
88,4.03710293584538,9174,8,1
```

## 📤 출력 (Output)

### 콘솔 출력

- 데이터 기본 정보 및 결측값
- 모델 성능 (정확도)
- Feature Importance 분석 결과
- 테스트 샘플 3개에 대한 개별 예측 기여도 분석

### 출력 파일

#### 1. `feature_importance_report.csv`

전체 모델의 Feature Importance 분석 결과입니다.

**컬럼 구성:**
- `Feature`: Feature 이름
- `Coefficient`: Logistic Regression 계수 값
- `Abs_Coefficient`: 계수의 절대값 (영향도 순위)
- `Impact`: 양의 영향 / 음의 영향

**위치:** 스크립트와 동일한 디렉토리

#### 2. `individual_contribution_{ID}.csv`

개인별 예측 기여도 분석 결과입니다. 각 테스트 샘플마다 개별 파일이 생성됩니다.

**컬럼 구성:**
- `Individual_ID`: 개인 식별자 (데이터 인덱스)
- `Feature`: Feature 이름
- `Feature_Value`: 해당 개인의 Feature 값
- `Coefficient`: 모델의 계수 값
- `Contribution`: 기여도 (Feature_Value × Coefficient)
- `Abs_Contribution`: 기여도의 절대값
- `Impact`: 증가 방향 / 감소 방향
- `Actual_Label`: 실제 정신 건강 상태
- `Predicted_Label`: 예측된 정신 건강 상태
- `Prediction_Probability`: 예측 확률 (1일 가능성)

**파일명 형식:** `individual_contribution_{인덱스번호}.csv`

**예시:** `individual_contribution_1234.csv`, `individual_contribution_5678.csv`

**위치:** 스크립트와 동일한 디렉토리

## 사용법

```bash
python train_model_new_data.py
```

스크립트 실행 시 자동으로 모델 훈련, 분석, 결과 저장이 수행됩니다.

## 주의사항

1. 입력 CSV 파일은 스크립트와 동일한 디렉토리에 위치해야 합니다
2. 데이터에 결측값이 없어야 합니다
3. `Mental_Health_Condition`은 0 또는 1의 값만 가져야 합니다