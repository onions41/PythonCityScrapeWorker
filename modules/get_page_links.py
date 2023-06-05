import sys
import re, logging
import requests
from urllib.parse import urlparse, parse_qs, urlencode
from time import sleep
from bs4 import BeautifulSoup
from .common.user_agents import get_useragent


# href is a full url string to the page that contains links to the resources
# yields the bytestring data of each resource
def get_page_links(href):
    print(href)
