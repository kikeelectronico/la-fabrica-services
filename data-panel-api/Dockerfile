FROM python:3.8-buster AS base
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD uvicorn main:app --host=0.0.0.0 --port=8000 --workers 1