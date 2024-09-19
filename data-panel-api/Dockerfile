FROM python:3.10.12-slim-bullseye
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD uvicorn main:app --host=0.0.0.0 --port=80 --workers 1