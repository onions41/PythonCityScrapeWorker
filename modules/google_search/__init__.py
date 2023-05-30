import re, logging
import requests
from time import sleep
from bs4 import BeautifulSoup
from common.user_agents import get_useragent

logger = logging.getLogger(__name__)


def search(search_string):
    # Sends search request to Google
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": get_useragent()
    }  # Random user agents from a list of possibles
    # Keep it simple. Using minimum params. num=25 because default is 10, which is too few
    params = {"q": search_string, "num": "25"}
    res = requests.get(base_url, params=params, headers=headers)

    # if res.status_code == not ok
    # should log the problem
    logger.info("Holy shat******")

    if res.text:
        soup = BeautifulSoup(res.text)

    # Check if there are no results found
    pattern = re.compile("your search.+did not match any documents", flags=re.I)
    for tag in soup.select("div.card-section"):
        if pattern.search(tag.find("p").text):
            return "no results"  # This is the value of the StopIteration exception

    # Yield search results
    result_block = soup.find_all("div", attrs={"class": "g"})
    for result in result_block:
        # Find link, title, description
        link = result.find("a", href=True)
        title = result.find("h3")
        description_box = result.find("div", {"style": "-webkit-line-clamp:2"})
        if description_box:
            description = description_box.text
            if link and title and description:
                yield {
                    "link_url": link["href"],
                    "link_title": title.text,
                    "link_description": description,
                }

    # Check if there is a next page
    pattern = re.compile("next$", flags=re.I)
    for tag in soup.find_all(
        lambda tag: tag.name == "div"
        and tag.has_attr("role")
        and tag["role"] == "navigation"
    ):
        if pattern.search(tag.text):
            yield
            # navigate to next page and rescurse
