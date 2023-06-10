# Built in modules
import re, logging
from time import sleep
from io import BytesIO

# External imports
import requests, fitz
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Internal imports
from .common.user_agents import get_useragent


# href is a full url string to the page that contains links to the pdf resources
# yields the bytestring data of each pdf, the url to the pdf, and the text extracted from pdf
def grab_pdfs(href):
    headers = {"User-Agents": get_useragent()}
    res = requests.get(href, headers=headers)

    if res.status_code != 200:
        logging.info("Status code not 200 for " + href)
        return "status code not 200"

    soup = BeautifulSoup(res.text, "html.parser")
    # type of document (minutes) is hardcoded TODO change when expanding app to analyse other documents
    pattern = re.compile("min\.pdf$", flags=re.I)
    links = soup.find_all("a", href=pattern)

    if not links:
        logging.info("No resources found in " + href)
        return "no resources found"

    for link in links:
        sleep(5)
        resource_url = urljoin(href, link["href"])
        res = requests.get(resource_url, headers=headers)
        if res.status_code == 200:
            logging.info("Got " + resource_url)
            # extract the text from res.content using fitz
            doc = fitz.open(stream=BytesIO(res.content))
            text_content = ""
            for page in doc.pages():
                text_content += page.get_text("text")

            yield {
                "resource_url": resource_url,
                "raw_data": res.content,
                "text_content": text_content,
            }
        else:
            logging.info("Status code not 200 for " + resource_url)
