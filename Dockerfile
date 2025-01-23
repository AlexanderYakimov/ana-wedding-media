FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
