FROM python:3.10-bullseye

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
WORKDIR /app
COPY Procfile .

ENTRYPOINT ["python"]