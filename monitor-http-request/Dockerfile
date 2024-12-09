FROM python:3.13.1-slim-bullseye
COPY . /app
WORKDIR /app
RUN mkdir audio
RUN pip install -r requirements.txt
CMD python main.py