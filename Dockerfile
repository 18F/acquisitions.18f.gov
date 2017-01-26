FROM python:3.5

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
