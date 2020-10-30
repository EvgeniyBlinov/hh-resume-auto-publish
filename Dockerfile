FROM python:3.9.0-alpine
RUN mkdir /app
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
