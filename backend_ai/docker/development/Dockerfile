FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY docker/scripts/ /app/docker/scripts/
RUN find /app/docker/scripts -name "*.sh" -exec chmod +x {} \;

COPY . .

ENTRYPOINT ["/app/docker/development/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]