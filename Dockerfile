FROM python:3.9-slim

WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app"

# Upgrade pip first
RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]