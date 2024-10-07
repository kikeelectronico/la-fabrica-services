FROM python:3.12.7-slim-bullseye
COPY . /app
WORKDIR /app
RUN mkdir audio
RUN pip install -r requirements.txt
CMD python main.py