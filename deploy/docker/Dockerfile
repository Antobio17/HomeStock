FROM python:3.9-slim

WORKDIR /app

COPY . /app/

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r deploy/docker/requirements.txt

CMD ["python", "src/app.py"]