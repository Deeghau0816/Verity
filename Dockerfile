FROM python:3.12-slim
WORKDIR /app
COPY requirements-collector.txt .
RUN pip install --no-cache-dir -r requirements-collector.txt
COPY data/ ./data/
CMD ["python", "data/collector.py"]
