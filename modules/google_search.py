import re, logging
import requests
from urllib.parse import urlparse, parse_qs
from time import sleep
from bs4 import BeautifulSoup
from .common.user_agents import get_useragent


# search_string is exactly what you would type into google
def search(search_string):
    # Sends search request to Google
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": get_useragent()
    }  # Random user agents from a list of possibles
    # Keep it simple. Using minimum params
    params = {"q": search_string}
    sleep(5)
    res = requests.get(base_url, params=params, headers=headers)

    # Loops until there are no more next pages.
    # Not using recursion, no need to crowd the stack.
    page = 1
    while True:
        if res.status_code != 200:
            logging.info("Status code not 200 for " + search_string)
            return "status code not 200"

        if res.text:
            soup = BeautifulSoup(res.text, "html.parser")

        # Check if there are no results found
        pattern = re.compile("your search.+did not match any documents", flags=re.I)
        for tag in soup.select("div.card-section"):
            if pattern.search(tag.find("p").text):
                logging.info("No results found for " + search_string)
                return "no results"

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

        logging.info("Searched " + search_string + ". Result yielded for page " + str(page))
        # Check if there is a next page
        pattern = re.compile("next$", flags=re.I)
        div_tag = soup.find(
            lambda tag: tag.name == "div"
            and tag.has_attr("role")
            and tag["role"] == "navigation"
            and pattern.search(tag.text)
        )

        # Means there is no next page
        if div_tag is None:
            logging.info("Hit Break")
            break

        next_link = div_tag.find(
            lambda tag: tag.name == "a" and pattern.search(tag.text)
        )

        # Parse out the next_link tag's href into params to use requests
        params = {}
        query_dict = parse_qs(urlparse(next_link["href"]).query)
        for k, v in query_dict.items():
            params[k] = v[0]

        page += 1
        sleep(5)  # Sleep 5 seconds. Not in a hurry, don't want to IP get banned.
        res = requests.get(base_url, params=params, headers=headers)
