# Backend Dockerfile
# First stage: build the frontend
FROM node:14 AS frontend-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Second stage: build the backend
FROM python:3.9
WORKDIR /app
COPY backend/requirements.txt .
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY backend/ .
COPY --from=frontend-build /app/build ./frontend/build
CMD ["python", "app.py"]
