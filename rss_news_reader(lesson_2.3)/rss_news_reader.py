import json
from collections import Counter
import re
import codecs

# компиляция выражений для удаления тэгов, пробельных символов
tags = re.compile('\<[^>]*\>')
reg = re.compile('\s|[,.;:«»/]')


def open_file_with_encoding(file_name, encoding_type):
    with codecs.open(file_name, encoding=encoding_type) as file_news:
        news_rss = json.load(file_news)
        print("\nКанал -", news_rss['rss']['channel']['title'], end='\n')
        return news_rss


def get_news_words_from_rss(news_rss):
    all_news_words = []
    greater_six_words = []
    for news in news_rss['rss']['channel']['item']:
        # обработка для файлов с разной структурой. newsit.json отличается от остальных
        try:
            tags_removed = tags.sub('', news['description']['__cdata'])
        except TypeError:
            tags_removed = tags.sub('', news['description'])
        words = tags_removed.split(' ')
        all_news_words.extend(words)
    # удаление слов длиной меньше шести символов
    for word in all_news_words:
        wordw = reg.sub('', word)
        if len(wordw) > 6:
            greater_six_words.append(wordw)
    return greater_six_words


def print_main_ten_words(file_name, encoding_type):
    news_rss = open_file_with_encoding(file_name, encoding_type)
    greater_six_words = get_news_words_from_rss(news_rss)
    # подсчет повторений и сортировка по убыванию
    dict_count = Counter(greater_six_words).most_common(10)
    for k, v in dict_count:
        print(k, end=' ')


print_main_ten_words('newsafr.json', "utf8")
print_main_ten_words('newscy.json', "koi8_r")
# Почему-то в json файле с новостями Франции новости Кипра
print_main_ten_words('newsfr.json', "iso8859_5")
print_main_ten_words('newsit.json', "cp1251")
