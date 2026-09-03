FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    U2NET_HOME=/models

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

RUN useradd --create-home --uid 10001 appuser && mkdir -p /models && chown -R appuser:appuser /models /app
USER appuser

EXPOSE 8830
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8830", "--no-access-log"]
