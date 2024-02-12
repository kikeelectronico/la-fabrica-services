FROM python:3.12.2-slim-bullseye
COPY . /app
WORKDIR /app
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/creds/data-panel-api.json"
RUN pip install -r requirements.txt
CMD uvicorn main:app --host=0.0.0.0 --port=80 --workers 1