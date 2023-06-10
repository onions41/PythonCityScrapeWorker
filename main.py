import os, sys, logging, re
import mysql.connector as database
import datetime
from dotenv import load_dotenv

# Internal imoports
from modules.google_search import search as google_search
from modules.grab_pdfs import grab_pdfs


# Let's try one where we start from an input search string "site:council.vancouver.ca/20230509 filetype:htm"
# then for each search result, insert a row for the meeting itself
# insert a row for each meeting record found
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
    cursor = connection.cursor()

    search_string = "site:council.vancouver.ca/20230509 filetype:htm"
    search_gen = google_search(search_string)

    phea_pattern = re.compile("/phea", flags=re.I)
    regu_pattern = re.compile("/regu", flags=re.I)
    spec_pattern = re.compile("/spec", flags=re.I)

    try: # TODO, this try cannot catch everything. divid it up so the nested looks have their own errors
        for result in search_gen:
            meeting_page_url = result["link_url"]
            # Determine the meeting type (TODO: move this out to its own module)
            meeting_type = ""
            if phea_pattern.search(meeting_page_url):
                meeting_type = "Public Hearing"
            elif regu_pattern.search(meeting_page_url):
                meeting_type = "Regular Council Meeting"
            elif spec_pattern.search(meeting_page_url):
                meeting_type = "Special Council Meeting"

            statement = """INSERT INTO meetings (municipality_name, meeting_date, meeting_type_name, meeting_url)
                VALUES (%s, %s, %s, %s)"""
            data = (
                "Vancouver",
                datetime.date(2023, 5, 9),
                meeting_type,
                meeting_page_url,
            )
            cursor.execute(statement, data)

            logging.info("Found meeting " + meeting_page_url)

            meeting_id = cursor.lastrowid
            resource_gen = grab_pdfs(meeting_page_url)
            try:
                for resource in resource_gen:
                    # TODO: Write the resource into the meeting_records table
                
                    statement = '''INSERT INTO meeting_records (meeting_id, record_type_name, data_url, raw_data, extracted_text)
                        VALUES (%s, %s, %s, %s, %s)'''
                    data = (
                        meeting_id,
                        "Minutes", # TODO
                        resource["resource_url"],
                        resource["raw_data"],
                        resource["text_content"]
                    )
                    cursor.execute(statement, data)
            except StopIteration as e:
                print("Stop iteration by grab_pdfs(): ", e)
    except StopIteration as e:
        print("Stop iteration by google_search(): ", e)
        connection.rollback()
    except database.Error as e:
        print("Database error: ", e)
        connection.rollback()
    except Exception as e:
        print("There was some other error: ", e)
        connection.rollback()
    else:
        connection.commit()
    finally:
        cursor.close()
        connection.close()


# def add_data(connection):
#     try:
#         statement = "INSERT INTO test_table (name) VALUES (%s)"
#         data = ("Santa2",)
#         connection.cursor().execute(statement, data)
#         connection.commit()
#         print("Successfully added entry to database")
#     except database.Error as e:
#         print(f"Error adding entry to database: {e}")


if __name__ == "__main__":
    logging.basicConfig(
        filename="worker.log",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
    main()
