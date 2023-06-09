import re, logging
import requests
from urllib.parse import urljoin
from time import sleep
from bs4 import BeautifulSoup
from .common.user_agents import get_useragent


# href is a full url string to the page that contains links to the resources
# yields the bytestring data of each resource
def grab_pdfs(href):
    headers = {"User-Agents": get_useragent()}
    res = requests.get(href, headers=headers)

    if res.status_code != 200:
        logging.info("Status code not 200 for " + href)
        return "status code not 200"

    soup = BeautifulSoup(res.text, "html.parser")
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
            yield {"resource_url": resource_url, "raw_data": res.content}
        else:
            logging.info("Status code not 200 for " + resource_url)
