import os
import sys
import mysql.connector as database
from dotenv import load_dotenv


def main():
    # Only load env vars if no argments are passed
    # Or, of arguments are passed only load env vars if the first arg isn't "production"
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != "production"):
        load_dotenv(".env.development")

    connection = database.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DATABASE_NAME"),
    )

    add_data(connection)


def add_data(connection):
    try:
        statement = "INSERT INTO test_table (name) VALUES (%s)"
        data = ("Santa2",)
        connection.cursor().execute(statement, data)
        connection.commit()
        print("Successfully added entry to database")
    except database.Error as e:
        print(f"Error adding entry to database: {e}")


if __name__ == "__main__":
    main()
