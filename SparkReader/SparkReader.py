import pyspark.sql.functions as functions
from pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext("local", "First App")
sqlContext = SQLContext(sc)
d1 = sqlContext.read.json('./CsvParser/resMyanimelist.json')
# date_end: bigint, date_start: bigint, episodes_cnt: bigint, members: bigint, page_num: bigint,
# score: string, title_en: string, type: string

d2 = sqlContext.read.json('./CsvParser/resShikimory.json')
# creator: string, date_start: bigint, duration: bigint, episodes_cnt: bigint, href: string,
# name_rus: string, name_rus_official: string, page_num: bigint, rating: string, score_ru: string, title_en: string,
# translator: string, type: string

cond = [functions.levenshtein(d1.title_en, d2.title_en) < 3,
        d1.date_start == d2.date_start]
join1 = d1.join(d2, cond, 'left_outer').select(functions.coalesce(d1.title_en, d2.title_en),
                                               d2.name_rus,
                                               functions.coalesce(d1.type, d2.type),
                                               functions.coalesce(d1.date_start, d2.date_start),
                                               functions.coalesce(d1.episodes_cnt, d2.episodes_cnt),
                                               d1.score,
                                               d2.score_ru,
                                               d2.creator,
                                               d2.duration,
                                               d1.date_end,
                                               d2.href,
                                               d1.members,
                                               d2.name_rus_official,
                                               d2.rating,
                                               d2.translator)
join2 = d1.join(d2, cond, 'right_outer').select(functions.coalesce(d1.title_en, d2.title_en),
                                                d2.name_rus,
                                                functions.coalesce(d1.type, d2.type),
                                                functions.coalesce(d1.date_start, d2.date_start),
                                                functions.coalesce(d1.episodes_cnt, d2.episodes_cnt),
                                                d1.score,
                                                d2.score_ru,
                                                d2.creator,
                                                d2.duration,
                                                d1.date_end,
                                                d2.href,
                                                d1.members,
                                                d2.name_rus_official,
                                                d2.rating,
                                                d2.translator)
union_df = join1.union(join2)
union_df = union_df \
    .withColumn('title_en', union_df['coalesce(title_en, title_en)']) \
    .withColumn('date_start', union_df['coalesce(date_start, date_start)']) \
    .withColumn('type', union_df['coalesce(type, type)']) \
    .withColumn('episodes_cnt', union_df['coalesce(episodes_cnt, episodes_cnt)']) \
    .drop('coalesce(title_en, title_en)') \
    .drop('coalesce(type, type)') \
    .drop('coalesce(date_start, date_start)') \
    .drop('coalesce(episodes_cnt, episodes_cnt)')

result = union_df \
    .groupBy(['type', 'creator', 'episodes_cnt']) \
    .agg(functions.avg('score'), functions.avg('score_ru'))
result = result \
    .withColumn('score', result['avg(score)']) \
    .withColumn('score_ru', result['avg(score_ru)']) \
    .drop('avg(score)') \
    .drop('avg(score_ru)')

with open("./SparkReader/result.json", "w") as output_file:
    output_file.write(str(result.toJSON().collect()).replace('\'', ''))
