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
dict_count = dict(Counter(greater_six_words))
a = sorted(dict_count.items(), key=lambda item: item[1], reverse=True)
print(a)
for k, v in a[0:10]:
    print(k, end=' ')
# не забыть по title для новостей!


