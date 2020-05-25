from abc import ABC

from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

keys = ['title_en',
        'type',
        'date_end',
        'episodes_cnt',
        'score',
        'page_num',
        'date_start',
        'members']


class CsvParserMyanimelist(MRJob, ABC):
    """
    Класс для преобразования csv с Myanimelist в json
    """
    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, _, line):
        csv_values = line[:-1].split(',')
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
                    if res_val.isdigit():
                        res_val = str(res_val)
                    else:
                        res_val = '"' + str(res_val) + '"'
                res += '"' + key + '": ' + res_val + ', '
            res = res[:-2] + '}'
        yield None, res

    def reducer(self, _, jsons):
        res_json = '['
        for json in jsons:
            if len(json):
                res_json += json + ','
        yield None, res_json[:-1] + ']'


if __name__ == '__main__':
    CsvParserMyanimelist.run()
