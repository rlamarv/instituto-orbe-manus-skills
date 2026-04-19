FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser --disabled-password --gecos '' appuser && mkdir -p /data/xml && chown -R appuser:appuser /app /data/xml

COPY . /app

USER appuser

CMD ["python", "-c", "print('omie-xml-intake base container ready')"]
