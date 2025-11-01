# Hack-heartai

웨어러블 기기 및 스마트폰 센서 데이터를 기반으로 정신 건강 상태를 예측하는 시스템입니다.

## 시스템 구조

```
Hack-heartai/
├── backend/          # FastAPI 백엔드 서버
├── frontend/         # React 프론트엔드
├── android/          # 안드로이드 앱 개발 가이드 및 예제 코드
├── model/            # 머신러닝 모델 학습 및 저장
└── data/             # SQLite 데이터베이스 (자동 생성)
```

## 주요 기능

### 1. 데이터 수집 (안드로이드 앱)
- 위치 데이터 (GPS)
- 스마트폰 사용 패턴
- 통화/SMS 빈도
- 신체 활동량 (걸음 수)
- 수면 패턴

### 2. 데이터 분석
- 주별 데이터 집계
- MADRS 점수 예측 (0-54점)
- 주요 행동 변화 인자 식별

### 3. 의료진용 보고서
- 예측된 MADRS 점수
- 주요 행동 변화 인자 그래프
- AI 모델 신뢰도 지수
- 권장사항 생성

## 시작하기

### 백엔드 설정

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### 프론트엔드 설정

```bash
cd frontend
npm install
npm run dev
```

### 안드로이드 앱 개발

`android/` 폴더의 가이드를 참고하여 안드로이드 앱을 개발하세요.

## API 엔드포인트

### 데이터 수집 (안드로이드 앱용)

- `POST /collect-sensor-data`: 단일 데이터 포인트 전송
- `POST /collect-sensor-data-batch`: 배치 데이터 전송
- `GET /get-daily-data/{patient_id}`: 일일 데이터 조회
- `GET /get-weekly-data/{patient_id}`: 주별 데이터 조회

### 분석 및 보고서

- `POST /analyze-weekly`: 주별 데이터 분석
- `POST /analyze-weekly-from-db/{patient_id}`: DB에서 자동 분석
- `POST /generate-report`: 의료진용 보고서 생성

## 안드로이드 앱 개발

안드로이드 앱에서 센서 데이터를 수집하여 백엔드로 전송하는 방법은 `android/README.md`를 참고하세요.

### 주요 구현 사항

1. **필수 권한**: 위치, 활동 인식, 통화/SMS 등
2. **데이터 수집**: GPS, 걸음 수, 스마트폰 사용량 등
3. **백그라운드 수집**: WorkManager를 사용한 주기적 데이터 수집
4. **오프라인 지원**: 네트워크 없을 때 로컬 저장 후 동기화

## 데이터 흐름

```
안드로이드 앱 → POST /collect-sensor-data → SQLite DB
                                              ↓
의료진 대시보드 → GET /get-weekly-data → POST /analyze-weekly-from-db
                                              ↓
                                          MADRS 예측 결과
                                              ↓
                                          보고서 생성
```

## 모델 학습

기존 모델을 사용하거나 새로운 데이터로 재학습:

```bash
cd model
python train_model.py
```

학습된 모델은 `model/model.joblib`에 저장되며, 백엔드가 자동으로 로드합니다.

## 배포 및 인프라

### 인프라 / 배포
- **AWS Lambda** (Container Image)
- **Amazon ECR**
- **GitHub Actions** (CI/CD)

### API 문서화
- **Swagger** (FastAPI 내장)

### 보안 / 인증
- **Lambda Function URL**

## 주의사항

- 프로덕션 환경에서는 CORS 설정을 제한해야 합니다
- HTTPS 사용 필수
- 환자 데이터 암호화 고려
- 개인정보 보호 관련 법규 준수
