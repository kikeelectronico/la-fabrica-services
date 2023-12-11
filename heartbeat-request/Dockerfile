FROM python:3.12.1-slim-bullseye
COPY . /app
WORKDIR /app
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/creds/heartbeat-request.json"
RUN pip install -r requirements.txt
CMD python main.py