import json
from pprint import pprint
from collections import Counter
import re
import codecs

reg = re.compile('\s|<br>|[,.;:«»/]')


def get_news_words_from_rss(news_rss):
    all_news_words = []
    greater_six_words = []
    for news in news_rss['rss']['channel']['item']:
        # pprint(news['description']['__cdata'])
        words = news['description']['__cdata'].split(' ')
        all_news_words.extend(words)
    print(all_news_words)
    for word in all_news_words:
        if len(word) > 6:
            wordw = reg.sub('', word)
            greater_six_words.append(wordw)
    print(greater_six_words)
    return greater_six_words


def print_main_ten_words(news_rss_file):
    greater_six_words = get_news_words_from_rss(news_rss_file)
    dict_count = dict(Counter(greater_six_words))
    main_words = sorted(dict_count.items(), key=lambda item: item[1], reverse=True)
    print(main_words)
    for k, v in main_words[0:10]:
        print(k, end=' ')

with open('newsafr.json') as file_news:
    news_rss = json.load(file_news)
    print("Канал -", news_rss['rss']['channel']['title'])
    # pprint(news_rss)

print_main_ten_words(news_rss)

with codecs.open('newscy.json', encoding="koi8_r") as cy_news:
    cy_news_rss = json.load(cy_news)
    print("\nКанал -", cy_news_rss['rss']['channel']['title'], end='\n')

print_main_ten_words(cy_news_rss)