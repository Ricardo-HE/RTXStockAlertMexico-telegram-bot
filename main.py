import os
import logging
import telegram
import time
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse

REQUEST_TIME = 420

URLS = ['https://ddtech.mx/producto/tarjeta-de-video-nvidia-geforce-rtx-3070-8gb-evga-ftw3-ultra-gaming-08g-p5-3767-kr-solo-1-por-cliente',
        'https://ddtech.mx/producto/tarjeta-de-video-nvidia-geforce-rtx-3070-8gb-gigabyte-vision-oc-gv-n3070vision-oc-8gd-solo-1-por-cliente',
        'https://ddtech.mx/producto/tarjeta-de-video-nvidia-geforce-rtx-3070-8gb-msi-ventus-2x-oc-912-v390-008-solo-1-por-cliente',
        'https://ddtech.mx/producto/tarjeta-de-video-nvidia-geforce-rtx-3070-8gb-evga-xc3-black-gaming-08g-p5-3751-kr-solo-1-por-cliente',
        'https://ddtech.mx/producto/tarjeta-de-video-nvidia-geforce-rtx-3070-8gb-gigabyte-gaming-oc-gv-n3070gamingoc-8gd-solo-1-por-cliente',
        'https://ddtech.mx/producto/tarjeta-de-video-nvidia-geforce-rtx-3070-8gb-zotac-twin-edge-oc-zt-a30700h-10p-solo-1-por-cliente',
        'https://ddtech.mx/producto/tarjeta-de-video-nvidia-geforce-rtx-3070-8gb-zotac-twin-edge-zt-a30700e-10p-solo-1-por-cliente',
        'https://ddtech.mx/producto/tarjeta-de-video-nvidia-geforce-rtx-3070-8gb-pny-dual-fan-vcg30708dfmpb-producto-aun-no-disponible-precio-estimado',
        'https://cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/GIGABYTE-TARJETA-DE-VIDEO-GeForce-RTX-3070-GAMING-OC-8G-WINDFORCE-3X-RGB-Fusion-2-0-GV-N3070GAMING-O.html',
        'https://cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-EVGA-NVIDIA-GeForce-RTX-3070-XC3-Black-Gaming-8GB-256-bit-GDDR6-PCI-Express-x16-4-0.html',
        'https://cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-Zotac-NVIDIA-GeForce-RTX-3070-Twin-Edge-8GB-256-bit-GDDR6-PCI-Express-x16-4-0.html',
        'https://cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-Gigabyte-Radeon-AMD-RX-5700-XT-GAMING-OC-8GB-256-bit-GDDR6-PCI-Express-x16-3-0.html',
        'https://cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-Sapphire-Pulse-AMD-Radeon-RX-5600-XT-BE-6GB-192-bit-GDDR6-PCI-Express-4-0.html']


def build_message(title, vendor, url, items_availables):
    message = "{0}\n{1} - Existen {2}\n{3}".format(vendor, title, items_availables, url)
    return message


def clean_html(raw_html):
    if raw_html is None:
        return None
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(raw_html))
    return cleantext


def clean_cyberpuerta_text(text):
    cleanr = re.compile('\d+')
    cleantext = cleanr.search(text).group()
    return cleantext


if __name__ == "__main__":

    # Load env variables
    load_dotenv()

    telegram_bot_token = os.getenv("TELEGRAM_ACCESS_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")

    # Create bot
    bot = telegram.Bot(token=telegram_bot_token)

    while True:
        time.sleep(REQUEST_TIME)
        for url in URLS:
            time.sleep(2)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'html.parser')
            url_parsed = urlparse(url)
            hostname = url_parsed.hostname
            if hostname == 'ddtech.mx':
                product = url_parsed.path.replace('/producto/', '')
                items_availables_raw = soup.find(
                    'span', attrs={'class': 'value'})
                items_availables = int(clean_html(items_availables_raw))
                if items_availables > 0:
                    message = build_message(
                        product, hostname, url, items_availables)
                    bot.send_message(chat_id=channel_id, text=message)
            elif hostname == 'cyberpuerta.mx':
                product = url_parsed.path.replace(
                    '/Computo-Hardware/Componentes/Tarjetas-de-Video/', '')
                product = product.replace('.html', '')
                items_availables_html_raw = soup.find(
                    'span', attrs={'class': 'stockFlag'})
                items_availables_raw = clean_html(items_availables_html_raw)
                if items_availables_raw is not None:
                    items_availables = int(
                        clean_cyberpuerta_text(items_availables_raw))
                    # I think if it reach this part is going to be always more than 1 but who knows
                    if items_availables > 0:
                        message = build_message(
                            product, hostname, url, items_availables)
                        bot.send_message(chat_id=channel_id, text=message)
