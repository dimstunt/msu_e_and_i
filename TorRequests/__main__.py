__author__ = 'dimstunt'

import csv

from TorRequests.ShikimoryParser import ShikimoriParser

PAGE_NUM_FIRST = 1
PAGE_NUM_LAST = 704


def main():
    shikimori_parser = ShikimoriParser()
    anime_list = []
    bad_html_list = []

    print("Парсим страницы со списком аниме")
    for page_num in range(PAGE_NUM_FIRST, PAGE_NUM_LAST + 1):
        print("Страница: {page_num} из {page_num_last}".format(page_num=page_num, page_num_last=PAGE_NUM_LAST))
        res_html, res_json_list = shikimori_parser.parse_anime_list(page_num)
        bad_html_cnt = 0
        for res_json in res_json_list:
            if 'href' not in res_json.keys():
                bad_html_cnt += 1
            else:
                anime_list.append(res_json)
            if bad_html_cnt:
                bad_html_list.append(res_html)
        if bad_html_cnt:
            print("\tНа странице {page_num} нет ссылок на {bad_html_cnt} аниме"
                  .format(page_num=page_num, bad_html_cnt=bad_html_cnt))

    len_anime = len(anime_list)
    len_bad_html = len(bad_html_list)
    print(("Все страницы распаршены, всего аниме {len_anime} шт.\n"
           "Нераспаршеных стианиц: {len_bad_html}"
           "Сохранение выкаченных названий\n").format(len_bad_html=len_bad_html, len_anime=len_anime))

    keys = set()
    for anime in anime_list:
        keys = keys.union(anime.keys())
    with open('shikimori_list.tsv', 'wt') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(anime_list)

    print("Выкаченные названия сохранены\n"
          "Выкачка инфе о каждом тайтле\n")

    for id_anime, anime in enumerate(anime_list):
        print('Аниме №{id_anime} из {len_anime}'.format(id_anime=id_anime + 1, len_anime=len_anime))
        res_html, res_json = shikimori_parser.parse_anime(anime['href'])
        # TODO обработать res_html
        anime.update(res_json)

    print("сохранение всех аниме")
    keys = set()
    for anime in anime_list:
        keys = keys.union(anime.keys())
    with open('shikimori_res.tsv', 'wt') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(anime_list)
    print("все аниме сохранены")


if __name__ == "__main__":
    main()
