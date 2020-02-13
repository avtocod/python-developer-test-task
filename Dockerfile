FROM python:3-alpine

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD python
