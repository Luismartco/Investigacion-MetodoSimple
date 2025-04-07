FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requeriments.txt


EXPOSE 8080

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:8080", "run:app"]