import re
from utility import clean_html


def scraper_ddtech(soup):
    stock_raw = soup.find(
        'span', attrs={'class': 'value'})
    if stock_raw is not None:
        stock = int(clean_html(stock_raw))
    else:
        stock = 0

    price_raw = soup.find(
        'span', attrs={'class': 'price'})
    price_raw = clean_html(price_raw)
    price = price_raw

    return stock, price


def scraper_cyberpuerta(soup):
    stock_raw = soup.find(
        'span', attrs={'class': 'stockFlag'})
    stock_raw = clean_html(stock_raw)
    if stock_raw is not None:
        cleanr = re.compile(r'\d+')
        stock = int(cleanr.search(stock_raw).group())
    else:
        stock = 0

    price_raw = soup.find(
        'span', attrs={'class': 'priceText'})
    price_raw = clean_html(price_raw)
    price = price_raw

    return stock, price


def get_scraper(store):
    scrapers = {
        "ddtech": scraper_ddtech,
        "cyberpuerta": scraper_cyberpuerta
    }

    return scrapers[store]
