FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

ENTRYPOINT ["python3"]

CMD ["manage.py", "runserver", "0.0.0.0:8000"]