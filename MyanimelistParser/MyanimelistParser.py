# -*- coding: utf-8 -*-
__author__ = 'dimstunt'

import logging

from bs4 import BeautifulSoup

from ConnectionManager import ConnectionManager

module_logger = logging.getLogger('MyanimelistParser')
module_logger.setLevel(logging.INFO)
fh = logging.FileHandler('log/MyanimelistParser.log', mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
module_logger.addHandler(fh)


class MyanimelistParser(ConnectionManager.ConnectionManager):
    def __init__(self):
        super().__init__()
        self._change_ip()

    def parse_anime_list(self, pn):
        """
        Парсит список аниме со страницы https://myanimelist.net/topanime.php?limit={pn}

        :param pn: номер страницы для парсинга
        :return: код страницы в виде текста, dict с названием аниме и ссылкой на ее страницу
        """
        logger = logging.getLogger("MyanimelistParser.parse_anime_list")
        logger.info(msg=f'Страница: {pn}')
        site = 'https://myanimelist.net/topanime.php?limit='
        if pn < 0 or pn > 334:
            logger.error(msg=f'error in parse_anime_list: wrong list_num {pn}')
            return None
        al = []
        r = self.request(f'{site}{pn * 50}')
        html = BeautifulSoup(r.content, 'html.parser')
        try:
            for el in html.select('.ranking-list'):
                kv = {'page_num': pn}
                detail = el.select_one('.detail')
                if detail:
                    clearfix = detail.select_one('.clearfix')
                    if clearfix:
                        hoverinfo_trigger = clearfix.select_one('.hoverinfo_trigger')
                        if hoverinfo_trigger:
                            kv['title_en'] = ''.join(ch for ch in hoverinfo_trigger.text if ch.isalpha()
                                                     or ch.isdigit()
                                                     or ch.isspace()).lower()
                    information = detail.select_one('.information')
                    if information:
                        params = information.text.split('\n')
                        if len(params) == 5:
                            kv['type'] = params[1].split('(')[0].strip()
                            kv['episodes_cnt'] = ''.join(ch for ch in params[1].split('(')[1] if ch.isdigit())
                            ds, de = params[2].split('-')
                            kv['date_start'] = ''.join(ch for ch in ds if ch.isdigit())
                            kv['date_end'] = ''.join(ch for ch in de if ch.isdigit())
                            kv['members'] = ''.join(ch for ch in params[3] if ch.isdigit())
                score = el.select_one('.score')
                if score:
                    score_label = score.select_one('.score-label')
                    if score_label:
                        kv['score'] = score_label.text
                al.append(kv)
        except Exception:
            logger.exception(msg=f'error in {site}{pn}')
        return r.text, al
