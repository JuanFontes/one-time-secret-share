FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and tests into the container image
COPY app/ .
COPY tests/ ./tests/

EXPOSE 5000
CMD ["python", "main.py"]
