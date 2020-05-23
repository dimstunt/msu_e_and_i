import requests
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller

with Controller.from_port(port=9051) as controller:
    controller.authenticate(password='dimstunt_local')
    print("Success!")
    controller.signal(Signal.NEWNYM)
    print("New Tor connection processed")
proxies = {'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/49.0.2623.87 Safari/537.36'
}
r = requests.get('https://shikimori.one/animes/page/1', headers=headers, proxies=proxies)
html = BeautifulSoup(r.content, 'html.parser')
for el in html.select('.title'):
    title_en = el.select_one('.name-en').text
    title_ru = el.select_one('.name-ru')['data-text']
    href = ''.join(['https://shikimori.one', el['href']])
    print(title_en, title_ru, href)

# for i in range(704)
# https://shikimori.one/animes/page/
