FROM python:3.13.3-slim-bullseye
COPY . /app
WORKDIR /app
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/creds/logger.json"
RUN pip install -r requirements.txt
CMD python main.py