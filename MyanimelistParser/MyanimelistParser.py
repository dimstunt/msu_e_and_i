# -*- coding: utf-8 -*-
__author__ = 'dimstunt'

from bs4 import BeautifulSoup
import logging
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
#
    def parse_anime_list(self, pn):
        """
        Парсит список аниме со страницы https://shikimori.one/animes/page/{page_num}

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
        r = self.request(f'{site}{pn*50}')
        html = BeautifulSoup(r.content, 'html.parser')
        try:
            for el in html.select('.ranking-list'):
                kv = {'page_num': pn}
                if detail := el.select_one('.detail'):
                    if clearfix := detail.select_one('.clearfix'):
                        if hoverinfo_trigger := clearfix.select_one('.hoverinfo_trigger'):
                            kv['en_name'] = hoverinfo_trigger.text
                    if information := detail.select_one('.information'):
                        params = information.text.split('\n')
                        if len(params) == 6:
                            kv['type'] = params[1].split('(')[0].strip()
                            kv['epizodes_cnt'] = ''.join(ch for ch in params[1].split('(')[1] if ch.isdigit())
                            kv['date'] = params[2]
                            kv['members'] = params[3]
                al.append(kv)
        except Exception:
            logger.exception(msg=f'error in {site}{pn}')
        return r.text, al
