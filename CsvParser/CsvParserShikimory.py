from abc import ABC

from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

keys = ['creator',
        'date_start',
        'duration',
        'episodes_cnt',
        'href',
        'name_rus',
        'name_rus_official',
        'page_num',
        'rating',
        'score_ru',
        'title_en',
        'translator',
        'type']


class CsvParserShikimory(MRJob, ABC):
    """
    Класс для преобразования csv с Myanimelist в json
    """
    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, _, line):
        def is_digit(string):
            if string.isdigit():
                return True
            else:
                try:
                    float(string)
                    return True
                except ValueError:
                    return False
        csv_values = line.split(',')
        d = dict(zip(keys, csv_values))
        if d[keys[0]] == keys[0]:
            res = ''
        else:
            res = '{'
            for key in d:
                if not d[key] or not len(d[key]):
                    res_val = 'null'
                else:
                    res_val = d[key].replace('"', '')
                    if is_digit(res_val):
                        res_val = str(float(res_val.replace(',', '.')))
                    else:
                        res_val = '"' + str(res_val) + '"'
                res += '"' + key + '": ' + res_val + ', '
            res = res[:-2] + '}'
        yield None, res

    def reducer(self, _, jsons):
        res_json = '['
        for json in jsons:
            if len(json):
                res_json += json + ', '
        yield None, res_json[:-2] + ']'


if __name__ == '__main__':
    CsvParserShikimory.run()
