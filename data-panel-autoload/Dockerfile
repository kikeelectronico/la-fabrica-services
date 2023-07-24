FROM python:3.11.4-slim-bullseye AS base
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python main.py