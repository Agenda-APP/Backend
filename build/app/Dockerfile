FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY build/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
