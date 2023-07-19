FROM python:3.10.12-slim-bullseye
COPY . /app
WORKDIR /app
RUN mkdir audio
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/creds/alert-system-request.json"
RUN pip install -r requirements.txt
CMD python main.py