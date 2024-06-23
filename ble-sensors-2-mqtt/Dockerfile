FROM python:3.12.4-bullseye
COPY . /app
WORKDIR /app
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/creds/ble-sensors-2-mqtt.json"
RUN pip install -r requirements.txt
CMD python main.py