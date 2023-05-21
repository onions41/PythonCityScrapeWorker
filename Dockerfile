FROM python:3.10-bullseye
RUN pip install -r requirements.txt

COPY . .
COPY Procfile .
WORKDIR /app

ENTRYPOINT ["python"]