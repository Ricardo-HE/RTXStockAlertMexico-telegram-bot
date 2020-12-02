import re
import yaml
import logging


def clean_html(raw_html):
    if raw_html is None:
        return None
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(raw_html))
    return cleantext


def update_item(item, stock, price):
    item["stock"] = stock
    item["price"] = price

    return item


def build_message(item, current_stock, current_price):
    if current_stock == 0 and item["stock"] > 0:
        message = "{} from {} has no stock anymore".format(
            item["name"], item["store"])
    else:
        message = """
            gpu: {}
            at: {}
            current stock: {}
            current price: {}
            url: {}
        """.format(
            item["name"],
            item["store"],
            current_stock,
            current_price,
            item["url"])

    return message


def initialize_items(yaml_file="items.yaml"):
    items = []
    with open(yaml_file) as f:
        gpus = yaml.load_all(f, Loader=yaml.FullLoader)
        for gpu in gpus:
            for name, stores in gpu.items():
                for store, urls in stores.items():
                    for url in urls:
                        items.append({
                            "name": name,
                            "store": store,
                            "url": url,
                            "stock": 0
                        })

    return items


def initialize_logger():
    # create a logger
    logger = logging.getLogger('mylogger')
    # set logger level
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('application_log.log')

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
