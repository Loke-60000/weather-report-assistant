FROM python:3.11-alpine

WORKDIR /app

COPY . /app

RUN apk add --no-cache postgresql-dev \
    && apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install sqlalchemy meteofrance-api psycopg2 \
    && apk del .build-deps

EXPOSE 5432


CMD ["python", "collect.py"]
