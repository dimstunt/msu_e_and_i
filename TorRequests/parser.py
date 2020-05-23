# -*- coding: utf-8 -*-
from dimstunt_0.ConnectionManager import ConnectionManager
from bs4 import BeautifulSoup


cm = ConnectionManager()
# for j in range(100):
#     for i in range(3):
#         print(cm.request("http://icanhazip.com/").text.strip())

r = cm.request('https://shikimori.one/animes/page/1')
html = BeautifulSoup(r.content, 'html.parser')
for el in html.select('.title'):
    title_en = el.select_one('.name-en').text
    title_ru = el.select_one('.name-ru')['data-text']
    href = ''.join(['https://shikimori.one', el['href']])
    print(title_en, title_ru, href)

# for i in range(704)
# https://shikimori.one/animes/page/
