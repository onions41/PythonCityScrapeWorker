FROM python:3.10-bullseye
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]