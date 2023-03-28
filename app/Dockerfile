FROM python:3.7

Run pip intall Flask
Run pip install firebase-admin
Run pip install datetime
Run pip install os
Run pip install uuid

COPY . /app
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app

# PAID DISCARDED