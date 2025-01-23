FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /env
ENV PATH="/env/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /env /env
COPY . /app

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py
ENV PATH="/env/bin:$PATH"

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
