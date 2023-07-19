FROM python:3.11-buster AS base
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python main.py