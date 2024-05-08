FROM --platform=linux/amd64 python:3.9.1

ENV PYTHONUNBUFFERED=1

WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
