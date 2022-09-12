import argparse

import requests
from bs4 import BeautifulSoup

from scraper.pages.status import (process_downstream_channel, process_upstream_channel,
                                  process_startup_procedure)
from scraper.setting import get_logger, BASE_URL

logger = get_logger(name='scraper.main')


def parse_page(page: str, url: str):
    logger.info(f"Parsing {url}")
    response = requests.get(url)
    if not response.ok:
        logger.error(f"Error parsing {url}. Response status code/reason: {response.status_code} - {response.reason}")
        return False
    return BeautifulSoup(response.content, "html.parser")


def process_page(page: str, content: str):
    logger.info(f"Processing {page}...")
    match page:
        case 'status':
            process_startup_procedure(content)
            process_downstream_channel(content)
            process_upstream_channel(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pages", help="Comma seperated list of pages to scrape")
    parser.add_argument("-u", "--base-url", help="Base URL of Arris SB6190 Modem")

    args = parser.parse_args()

    # Set pages to scrape
    pages = args.pages

    # Set base_url
    base_url = BASE_URL
    if args.base_url:
        base_url = args.base_url

    for page in pages.split(","):
        url = ''
        match page:
            case 'status':
                url = f"{base_url}/cgi-bin/status"
            case 'swinfo':
                logger.info(f"Sorry, this app does not scrape '{base_url}/{page}' yet")
            case _:
                logger.error(f"Page not found. Are you sure '{base_url}/{page}' is valid?")

        if url:
            content = parse_page(page, url)
            result = process_page(page, content)

    logger.info("Done!")
