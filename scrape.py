import os
import sys
import mysql.connector as database
from dotenv import load_dotenv

def scrape():
    # Only load env vars if no argments are passed
    # Or, of arguments are passed only load env vars if the first arg isn't "production"
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != "production"):
        load_dotenv(".env.development")
        print("this is dev environment")

    # if __name__ == "__main__":
    #     connection = database.connect(
    #         user="city_scrape",
    #         password="itdoesntmatter",
    #         host="127.0.0.1",
    #         port="3306",
    #         database="city_scrape",
    #     )

    print(sys.argv)
    print(os.getenv("DB_USER"))
    print(os.getenv("DB_PASSWORD"))
    print(os.getenv("DB_HOST"))
    print("hello there")

if __name__ == "__main__":
    scrape()
