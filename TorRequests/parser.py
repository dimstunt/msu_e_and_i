# -*- coding: utf-8 -*-
__author__ = 'dimstunt'

from TorRequests.ConnectionManager import ConnectionManager
from bs4 import BeautifulSoup
# import json
# from bs4.element import Tag
# from requests import Response


class Shikimori(ConnectionManager):
    def __init__(self):
        super().__init__()
        self.cm = ConnectionManager()
        self.html = BeautifulSoup('<a>null</a>', 'html.parser')

    def parse_anime_list(self, page):
        """
        Парсит список аниме со страницы https://shikimori.one/animes/page/list_num
        """
        site = 'https://shikimori.one/animes/page/'
        if page < 1 or page > 704:
            print("error in parse_anime_list: wrong list_num")
            return None
        # TODO обработать ошибку
        al = []
        r = self.cm.request('{site}{page}'.format(site=site, page=page))
        self.html = BeautifulSoup(r.content, 'html.parser')
        # TODO убрать html из класса после отладки
        try:
            for el in self.html.select('.c-anime'):
                kv = {}
                kv['title_en'] = el.select_one('.name-en').text
                kv['title_ru'] = el.select_one('.name-ru')['data-text']
                kv['href'] = el.select_one('.cover')['href']
                al.append(kv)
        except:
            print("error in {site}{page}".format(site=site, page=page))
        return al

    def parse_anime(self, url):
        r = self.cm.request(url)
        self.html = BeautifulSoup(r.content, 'html.parser')
        kv = {}
        for line in self.html.select('.line-container'):
            if key := line.select_one('.key'):
                # print("ключ ", [line.select_one('.key'), key])
                if (key := key.text.replace(u'\xa0', u' ').strip(':')) not in ('Жанры', 'Альтернативные названия'):
                    # print("текст ключа ", key)
                    if value := line.select_one('.value'):
                        # print([key, value, value.text])
                        kv[key] = value.text.replace(u'\xa0', u' ').strip()
        if val := self.html.select_one('.text-score').select_one('.score-value'):
            kv['Оценка'] = val.text.replace(u'\xa0', u' ').strip()
        if (val := self.html.select_one('.studio-logo')) and val.has_attr('alt'):
            kv['Студия'] = val['alt'].replace(u'\xa0', u' ').strip()
        # print(kv)
        return kv


shikimori = Shikimori()
# for
anime_list = shikimori.parse_anime_list(100)
for anime in anime_list:
    anime.update(shikimori.parse_anime(anime['href']))
    print(anime)

# rr = json.dumps(kv, ensure_ascii=False)
# json.dump(kv)
# for i in range(704)
# https://shikimori.one/animes/page/
