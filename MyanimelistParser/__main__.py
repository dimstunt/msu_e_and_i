__author__ = 'dimstunt'

import csv
import logging
import os
import shutil

import MyanimelistParser

PAGE_NUM_FIRST = 0
PAGE_NUM_LAST = 334


def main():
    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('log/main.log', mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if os.path.exists('bad_html'):
        shutil.rmtree('bad_html', ignore_errors=True)
    os.mkdir('bad_html')

    myanimelist_parser = MyanimelistParser.MyanimelistParser()
    anime_list = []

    logger.info(msg='Парсим страницы со списком аниме')
    logger.info(msg=f'Страницы с {PAGE_NUM_FIRST} по {PAGE_NUM_LAST}')
    for page_num in range(PAGE_NUM_FIRST, PAGE_NUM_LAST + 1):
        res_html, res_json_list = myanimelist_parser.parse_anime_list(page_num)
        anime_list.extend(res_json_list)

    len_anime = len(anime_list)
    logger.info(msg=f'Все страницы обработаны, аниме распаршено {len_anime} шт.')
    logger.info(msg=f'Сохранение всех аниме')

    keys = set()
    for anime in anime_list:
        keys = keys.union(anime.keys())
    keys = list(keys)
    keys.sort()
    with open('myanimelist_res.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(anime_list)

    logger.info(msg=f'все аниме сохранены')


if __name__ == "__main__":
    main()
