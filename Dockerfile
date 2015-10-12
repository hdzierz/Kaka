FROM python:2.7

MAINTAINER helge.dzierzon@plantandfood.co.nz

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y; \
	apt-get upgrade -y; \
	apt-get install wget;

RUN mkdir /code
WORKDIR /code
ADD requirements_pinf.txt /code/requirements.txt

RUN pip install -r requirements.txt
RUN git clone https://github.com/hdzierz/pinf.git; \
	cd pinf; \

