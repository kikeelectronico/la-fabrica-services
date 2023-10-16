FROM python:3.12.0-slim-bullseye
COPY . /app
WORKDIR /app
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/creds/heartbeat-monitor.json"
RUN pip install -r requirements.txt
CMD python main.py