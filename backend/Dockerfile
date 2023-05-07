# Backend Dockerfile
# First stage: build the frontend
FROM node:14 AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Second stage: build the backend
FROM python:3.9
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
COPY --from=frontend-build /frontend/build /app/frontend/build
CMD ["python", "__init__.py"]
