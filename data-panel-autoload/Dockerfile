FROM python:3.12.1-slim-bullseye AS base
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python main.py