FROM python:3.8-buster
COPY . /app
WORKDIR /app
RUN mkdir audio
RUN mkdir creds
RUN pip install -r requirements.txt
CMD python main.py