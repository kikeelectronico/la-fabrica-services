FROM python:3.8-buster
COPY ./mqtt-2-bigquery /app
WORKDIR /app
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/creds/creds.json
#RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python mqtt-2-bigquery.py