import argparse

import requests
from bs4 import BeautifulSoup

from influxdb import send_metrics
from setting import get_logger, BASE_URL

logger = get_logger(name='scraper.main')


def parse_page(url: str):
    logger.info(f"Parsing {url}")
    response = requests.get(url)
    if not response.ok:
        logger.error(f"Error parsing {url}. Response status code/reason: {response.status_code} - {response.reason}")
        return False
    return BeautifulSoup(response.content, "html.parser")


def process_page(content: str):
    page_title = content.title.string
    tables = content.find_all('table')

    for table in tables[1:]:  # Skip the first table (table[0]) since it's hidden
        rows = table.find_all('tr')
        headers = rows[1].find_all('td')
        key = headers[0].string

        tags = {
            "Page": page_title,
            "Table": table.th.string,  # same as rows[0].th.string
            key: ""  # for example: `"Channel": "0"`
        }

        for row in rows[2:]:  # Start at rows[2] - rows[0] is the table header and rows[1] are the column names
            column = row.find_all('td')
            tags[key] = column[0].string
            stats = {}
            for i in range(len(headers)):
                stats[headers[i].string] = column[i].string
            logger.info(f"Tags: {tags}")
            logger.info(f"Stats: {stats}")
            send_metrics(tags, stats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pages", help="Comma seperated list of pages to scrape")
    parser.add_argument("-u", "--base-url", help="Base URL of Arris SB6190 Modem")

    args = parser.parse_args()

    pages = args.pages

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
            content = parse_page(url)
            result = process_page(content)

    logger.info("Done!")
