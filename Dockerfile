FROM python:3.12-slim as builder
LABEL author="Y-Humble"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERD 1

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --without dev,test

FROM builder as dev

EXPOSE 8080

COPY . .

RUN chmod a+x src/scripts/*.sh
