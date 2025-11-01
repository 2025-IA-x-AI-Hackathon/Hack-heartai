FROM public.ecr.aws/lambda/python:3.11

WORKDIR /var/task

COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir -r requirements.txt && \
    python -m pip install --no-cache-dir mangum==0.17.0

COPY backend /var/task/backend
COPY model /var/task/model
COPY lambda_app.py /var/task/lambda_app.py

# FastAPI는 lambda_app.handler 로 진입
CMD ["lambda_app.handler"]
