FROM python:3-alpine

COPY ./requirements.txt /requirements.txt
COPY ./requirements-dev.txt /requirements-dev.txt

RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . /app
WORKDIR /app

CMD python
