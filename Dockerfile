FROM python:3.10-bullseye
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV DB_USER="city_scrape"
ENV DB_PASSWORD="itdoesntmatter"
ENV DB_HOST="127.0.0.1"
ENV DB_PORT="3306"
ENV DATABASE_NAME="city_scrape"

ENTRYPOINT ["python", "scrape.py", "production"]