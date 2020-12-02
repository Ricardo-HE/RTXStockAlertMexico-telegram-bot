#!/usr/bin/env python3

import os
import logging
import time
import telegram
import random

from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

from scrapers import get_scraper
from utility import initialize_items
from utility import initialize_logger
from utility import update_item
from utility import build_message

MIN_WAIT_TIME = 5
MAX_WAIT_TIME = 30
WAIT_BETWEEN_REQUESTS = 5


def check_availability(item, logger=None):
    stock = None
    price = None

    r = requests.get(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code != 200:
        if logger:
            logging.warning(
                "Got {} status code in {}".format(r.status_code, item["url"])
            )

        return stock, price

    webpage = r.text
    soup = BeautifulSoup(webpage, 'html.parser')

    scraper = get_scraper(item["store"])
    stock, price = scraper(soup)

    return stock, price


##############################################################################

if __name__ == "__main__":
    load_dotenv()
    logger = initialize_logger()
    telegram_bot_token = os.getenv("TELEGRAM_ACCESS_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    bot = telegram.Bot(token=telegram_bot_token)

    items = initialize_items("items.yaml")

    logger.info("Starting application")
    while(True):
        for item in items:
            current_stock, current_price = check_availability(item, logger)

            if current_stock is None or current_price is None:
                message = "Got {} stock and {} price " \
                    "for {} at {} with url {}" \
                    .format(
                        current_stock,
                        current_price,
                        item["name"],
                        item["store"],
                        item["url"]
                    )
                logger.warning(message)
                continue

            if (item["stock"] == 0 and current_stock > 0 or
                    item["stock"] > 0 and current_stock == 0):
                update_item(item, current_stock, current_price)
                message = build_message(item, current_stock, current_price)
                bot.send_message(chat_id=chat_id, text=message)
                logger.info(message)

            time.sleep(WAIT_BETWEEN_REQUESTS)

    time.sleep(random.randint(MIN_WAIT_TIME, MAX_WAIT_TIME))
