FROM python:3.9.1

ENV PYTHONUNBUFFERED=1

WORKDIR /api
COPY . /api/
RUN pip install -r requirements.txt

# Place to store static files
RUN mkdir /frontend
RUN mkdir /frontend/public

# Cron
RUN apt-get update && apt-get install -y cron
COPY api/jobs/cron/hourly-tasks /etc/cron.d/hourly-tasks