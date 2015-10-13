FROM python:2.7

MAINTAINER helge.dzierzon@plantandfood.co.nz

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
