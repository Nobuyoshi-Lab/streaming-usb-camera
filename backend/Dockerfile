FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY --from=frontend:latest /frontend/build /app/frontend/build

CMD ["python", "__init__.py"]
