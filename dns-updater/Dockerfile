FROM python:3.12.3-slim-bullseye
COPY . /app
WORKDIR /app
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/creds/dns-updater.json"
RUN pip install -r requirements.txt
CMD python main.py