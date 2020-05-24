# -*- coding: utf-8 -*-
__author__ = 'dimstunt'

from bs4 import BeautifulSoup

# logger
# ipdb
from TorRequests.ConnectionManager import ConnectionManager


class ShikimoriParser(ConnectionManager):
    def __init__(self):
        super().__init__()
        self.cm = ConnectionManager()

    def parse_anime_list(self, pn):
        """
        Парсит список аниме со страницы https://shikimori.one/animes/page/{page_num}

        :param pn: номер страницы для парсинга
        :return: dict с названием аниме и ссылкой на ее страницу
        """
        site = 'https://shikimori.one/animes/page/'
        if pn < 1 or pn > 704:
            print("error in parse_anime_list: wrong list_num")
            return None
        # TODO обработать ошибку
        al = []
        r = self.cm.request('{site}{page_num}'.format(site=site, page_num=pn))
        html = BeautifulSoup(r.content, 'html.parser')
        # TODO убрать html из класса после отладки
        try:
            for el in html.select('.c-anime'):
                kv = {'page_num': pn}
                if title_en := el.select_one('.name-en'):
                    kv['title_en'] = title_en.text.replace(u'\xa0', u' ').strip('')
                if (title_ru := el.select_one('.name-ru')) and title_ru.has_attr('data-text'):
                    kv['title_ru'] = title_ru['data-text'].replace(u'\xa0', u' ').strip('')
                if (href := el.select_one('.cover')) and href.has_attr('href'):
                    kv['href'] = href['href'].replace(u'\xa0', u' ').strip('')
                al.append(kv)
        except Exception as e:
            print("\terror in {site}{page}: {e}".format(e=e, site=site, page=pn))
            # TODO обработать ошибки
        return html, al

    def parse_anime(self, url):
        """
        Парсит информацию об аниме со страницы с описанием аниме
        :param url: url страницы
        :return: словарь с полной информацией об аниме-тайтле
        """
        if url is None:
            return None
        r = self.cm.request(url)
        html = BeautifulSoup(r.content, 'html.parser')
        kv = {}
        for line in html.select('.line-container'):
            if key := line.select_one('.key'):
                # print("ключ ", [line.select_one('.key'), key])
                if (key := key.text.replace(u'\xa0', u' ').strip(':')) not in ('Жанры', 'Альтернативные названия'):
                    # print("текст ключа ", key)
                    if value := line.select_one('.value'):
                        # print([key, value, value.text])
                        kv[key] = value.text.replace(u'\xa0', u' ').strip()
        if val := html.select_one('.text-score').select_one('.score-value'):
            kv['Оценка'] = val.text.replace(u'\xa0', u' ').strip()
        if (val := html.select_one('.studio-logo')) and val.has_attr('alt'):
            kv['Студия'] = val['alt'].replace(u'\xa0', u' ').strip()
        # print(kv)
        return html, kv
