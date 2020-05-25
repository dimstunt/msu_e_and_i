# -*- coding: utf-8 -*-
__author__ = 'dimstunt'

import logging
import re

from bs4 import BeautifulSoup

from ConnectionManager import ConnectionManager

module_logger = logging.getLogger('ShikimoryParser')
module_logger.setLevel(logging.INFO)
fh = logging.FileHandler('log/ShikimoryParser.log', mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
module_logger.addHandler(fh)


class ShikimoryParser(ConnectionManager.ConnectionManager):
    def __init__(self):
        super().__init__()
        self._change_ip()

    def parse_anime_list(self, pn):
        """
        Парсит список аниме со страницы https://shikimori.one/animes/page/{page_num}

        :param pn: номер страницы для парсинга
        :return: код страницы в виде текста, dict с названием аниме и ссылкой на ее страницу
        """
        logger = logging.getLogger("ShikimoryParser.parse_anime_list")
        logger.info(msg=f'Страница: {pn}')
        site = 'https://shikimori.one/animes/page/'
        if pn < 1 or pn > 704:
            logger.error(msg=f'error in parse_anime_list: wrong list_num {pn}')
            return None
        al = []
        r = self.request(f'{site}{pn}')
        html = BeautifulSoup(r.content, 'html.parser')
        try:
            for el in html.select('.c-anime'):
                kv = {'page_num': pn}
                title_en = el.select_one('.name-en')
                if title_en:
                    kv['title_en'] = ''.join(ch for ch in title_en.text.replace(u'\xa0', u' ')
                                             if ch.isalpha()
                                             or ch.isdigit()
                                             or ch.isspace()).lower()
                title_ru = el.select_one('.name-ru')
                if title_ru and title_ru.has_attr('data-text'):
                    kv['name_rus'] = title_ru['data-text'].replace(u'\xa0', u' ').strip('')
                href = el.select_one('.cover')
                if href:
                    if href.has_attr('href'):
                        kv['href'] = href['href'].replace(u'\xa0', u' ').strip('')
                    elif href.has_attr('data-href'):
                        kv['href'] = href['data-href'].replace(u'\xa0', u' ').strip('')
                al.append(kv)
        except Exception:
            logger.exception(msg=f'error in {site}{pn}')
        return r.text, al

    def parse_anime(self, url):
        """
        Парсит информацию об аниме со страницы с описанием аниме
        :param url: url страницы
        :return: словарь с полной информацией об аниме-тайтле
        """
        if url is None:
            return None
        r = self.request(url)
        html = BeautifulSoup(r.content, 'html.parser')
        kv = {}
        types = {'TV Сериал': 'TV', 'Фильм': 'Movie', 'Спешл': 'Special', 'Клип': 'Music'}
        for line in html.select('.line-container'):
            key = line.select_one('.key')
            if key:
                # print("ключ ", [line.select_one('.key'), key])
                key = key.text.replace(u'\xa0', u' ').strip(':')
                if key not in ('Жанры', 'Альтернативные названия'):
                    # print("текст ключа ", key)
                    value = line.select_one('.value')
                    if value:
                        if key == 'Тип':
                            val = value.text.replace(u'\xa0', u' ').strip()
                            if val in types:
                                kv['type'] = types[val]
                        elif key == 'Эпизоды':
                            kv['episodes_cnt'] = value.text.replace(u'\xa0', u' ').strip()
                        elif key == 'Длительность эпизода':
                            val = value.text.replace(u'\xa0', u' ').strip()
                            regex = re.search(r'(([0-9])+ часа? )?([0-9]+) мин', val)
                            if regex:
                                dur = regex.group(2, 3)
                                kv['duration'] = int(dur[0] or 0) * 60 + int(dur[1])
                        elif key == 'Статус':
                            val = value.text.replace(u'\xa0', u' ').strip()
                            if re.search(r'в ([0-9]{4})-[0-9]+', val):
                                regex = re.search(r'в ([0-9]{4})-[0-9]+', val)
                                kv['date_start'] = regex.group(1)
                            elif re.search(r'([0-9]{4}) г. по', val):
                                regex = re.search(r'([0-9]{4}) г. по', val)
                                kv['date_start'] = regex.group(1)
                            elif re.search(r'([0-9]{4})', val):
                                regex = re.search(r'([0-9]{4})', val)
                                kv['date_start'] = regex.group(1)
                        elif key == 'Рейтинг':
                            kv['rating'] = value.text.replace(u'\xa0', u' ').strip()
                        elif key == 'Лицензировано в РФ под названием':
                            kv['name_rus_official'] = value.text.replace(u'\xa0', u' ').strip()
                        elif key == 'Лицензировано':
                            kv['translator'] = value.text.replace(u'\xa0', u' ').strip()
                        # print([key, value, value.text])
        text_score = html.select_one('.text-score')
        if text_score:
            score_value = text_score.select_one('.score-value')
            if score_value:
                kv['score_ru'] = score_value.text.replace(u'\xa0', u' ').strip()
        val = html.select_one('.studio-logo')
        if val and val.has_attr('alt'):
            kv['creator'] = re.search(r'Аниме студии (.*)', val['alt'].replace(u'\xa0', u' ').strip()).group(1)
        # print(kv)
        return r.text, kv
