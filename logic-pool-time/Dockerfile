FROM python:3.11.4-slim-bullseye
COPY . /app
WORKDIR /app
RUN mkdir creds
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/creds/logic-pool-time.json"
RUN pip install -r requirements.txt
CMD python main.py