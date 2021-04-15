FROM python:3.8-buster

RUN mkdir api
WORKDIR /api
RUN mkdir instance

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY api/ api/

CMD gunicorn "api:create_app()" -w 2 -b 0.0.0.0:8000