FROM python:3.9.21-slim

RUN apt-get update && \
    pip install poetry

WORKDIR /app

COPY . /app/

ENV PYTHONPATH=/app

RUN poetry config virtualenvs.create false && \
    poetry install

CMD ["python", "src/app.py"]