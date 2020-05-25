__author__ = 'dimstunt'

import csv
import logging
import os
import shutil

import ShikimoryParser

PAGE_NUM_FIRST = 1
PAGE_NUM_LAST = 704


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

    shikimory_parser = ShikimoryParser.ShikimoryParser()
    anime_list = []
    bad_html_list = []

    logger.info(msg='Парсим страницы со списком аниме')
    logger.info(msg=f'Страницы с {PAGE_NUM_FIRST} по {PAGE_NUM_LAST}')
    for page_num in range(PAGE_NUM_FIRST, PAGE_NUM_LAST + 1):
        res_html, res_json_list = shikimory_parser.parse_anime_list(page_num)
        bad_html_cnt = 0
        for res_json in res_json_list:
            if 'href' not in res_json.keys():
                bad_html_cnt += 1
            else:
                anime_list.append(res_json)
            if bad_html_cnt:
                bad_html_list.append(res_html)
        if bad_html_cnt:
            logger.warning(msg=f'На странице {page_num} нет ссылок на {bad_html_cnt} аниме')
            with open(f'bad_html/{page_num}.html', 'w') as output_file:
                output_file.write(res_html)

    len_anime = len(anime_list)
    len_bad_html = len(bad_html_list)
    logger.info(msg=f'Все страницы обработаны, аниме распаршено {len_anime} шт.')
    if len_bad_html:
        logger.warning(msg=f'Нераспаршеных стианиц: {len_bad_html}')
    logger.info(msg=f'Сохранение выкаченных названий')

    keys = set()
    for anime in anime_list:
        keys = keys.union(anime.keys())
    with open('shikimory_list.tsv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(anime_list)

    logger.info(msg=f'Выкаченные названия сохранены')
    logger.info(msg=f'Выкачка инфы о каждом тайтле')

    for id_anime, anime in enumerate(anime_list):
        if id_anime % 50 == 49:
            logger.info(msg=f'Аниме №{id_anime + 1} из {len_anime}')
        res_html, res_json = shikimory_parser.parse_anime(anime['href'])
        anime.update(res_json)

    logger.info(msg=f'сохранение всех аниме')
    keys = set()
    for anime in anime_list:
        keys = keys.union(anime.keys())
    with open('shikimory_res.tsv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(anime_list)
    logger.info(msg=f'все аниме сохранены')


if __name__ == "__main__":
    main()
