import requests
import json
import time
from collections import Counter


def list_div(list_for_split, n=25):
    return [list_for_split[i:i + n] for i in range(0, len(list_for_split), n)]

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.63'
APP_ID = 5863643
api_address = 'https://api.vk.com/method/'
access_token = '76e01e83604e3f9e6527ab13fb0320d4cefd4fa8424a93c3f6032c1f94096f9d09b7fd1bcd0954a9b54db'
# TODO не забыть сделать input для введения id
print("Введите id интересующей личности:")
user_id = input()
params = {
    'user_id': user_id,
    'access_token': access_token,
    'v': VERSION
}

# TODO обработать исключения которые возникают при запрете на получение списка друзей
# получаем список друзей
friends_method = 'friends.get'
response1 = requests.get(api_address + friends_method, params)
try:
    friends_list = response1.json()['response']['items']
    print("Количество друзей:", len(friends_list))
except KeyError:
    friends_list = []
    print("Список друзей закрыт")

# получаем количество подписчиков
# TODO выводить сколько обработано подписчиков из общего коичества
followers_method = 'users.getFollowers'
response2 = requests.get(api_address + followers_method, params)
followers_count = response2.json()['response']['count']
print("Общее количество подписчиков:", followers_count)

# получаем список подписчиков
# TODO завернуть этот метод в execute иначе будет слишком долго
all_followers = []
offset_parm = 0
print("Получаю список подписчиков...")
for i in range(followers_count // 1000 + 1):
    params = {
        'user_id': user_id,
        'access_token': access_token,
        'v': VERSION,
        'offset': offset_parm,
        'count': 1000
    }
    response3 = requests.get(api_address + followers_method, params)
    followers_list = response3.json()['response']['items']
    all_followers.extend(followers_list)
    offset_parm += 1000
    time.sleep(.200)

all_followers.extend(friends_list)
# print(all_followers)
all_followers_count = len(all_followers)
divided_list = list_div(all_followers)

method = 'execute?access_token=' + access_token + '&code='
print("Обработка групп, в которых состоят подписчики ...")
merge_list = []
user_count = 0
for l in divided_list:
    code = 'return ['
    user_count += 25
    remain_to_calc = all_followers_count - user_count
    if remain_to_calc > 0:
        print("Осталось обработать %s из %s подписчиков" % (remain_to_calc, all_followers_count))
    else:
        print("Обработка почти завершена =))", end='\n')
    for user_id in l:
        code = '%s%s' % (code, 'API.groups.get({"user_id":%s}),' % str(user_id))
    code = '%s%s' % (code, '];')
    r = requests.get(api_address + method + code).json()['response']
    for i in r:
        if type(i) == type(True):
            r.remove(i)
        else:
            merge_list.append(i)
# print(merge_list)
full_merge_list = sum(merge_list, [])
# print(full_merge_list)
print("Топ 100 групп, в которых состоят подписчики:", end='\n')
top_groups = Counter(full_merge_list).most_common(100)
# print(top_groups)
top_groups_list = []
for group, k in top_groups:
    group_name_method = 'groups.getById'
    params = {
        'access_token': access_token,
        'v': VERSION,
        'group_id': group
    }
    response4 = requests.get(api_address + group_name_method, params)
    name = response4.json()['response'][0]['name']
    print(name, k)
    a = {'title': name, 'count': k, 'id': group}
    top_groups_list.append(a)
    time.sleep(.200)
top_100 = json.dumps(top_groups_list, ensure_ascii=False)
print('\n'"Формирование файла top100.json", )
with open("top100.json", 'w') as t:
    t.write(top_100)

# TODO вторая часть - получить 5 первыйх групп и инфу о их подписчиках метод groups.getMembers
