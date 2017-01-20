import json
from pprint import pprint
from collections import Counter, OrderedDict
import re


reg = re.compile('\s|<br>|[,.;:«»]')

with open("newsafr.json") as afr_news:
    afr = json.load(afr_news)
   # pprint(afr)

all_news_words = []
greater_six_words = []

for news in afr['rss']['channel']['item']:
    # pprint(news['description']['__cdata'])
    words = news['description']['__cdata'].split(' ')
    all_news_words.extend(words)

for word in all_news_words:
    if len(word) > 6:
        wordw = reg.sub('', word)
        greater_six_words.append(wordw)

print(greater_six_words)
print(len(greater_six_words))

# # print(Counter(all_news_words))
# dict_count = dict(Counter(all_news_words))
# print(dict_count)
# l = lambda x: len(x[0]) > 6
# a = sorted(dict_count.items(), key=l)
# print(a)