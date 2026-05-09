FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# OpenCV (cv2) often needs these shared libraries on Debian slim.
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libgl1 \
    libgomp1 \
  && rm -rf /var/lib/apt/lists/*

COPY backend /app/backend
COPY frontend /app/frontend

WORKDIR /app

ENV MODEL_PATH=/app/backend/models/best.pt
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "-m", "backend.app.main"]
