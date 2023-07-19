FROM python:3.11-buster
COPY . /app
WORKDIR /app
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/creds/mqtt-2-hue.json"
RUN pip install -r requirements.txt
CMD python main.py