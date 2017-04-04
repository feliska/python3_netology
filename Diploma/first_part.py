import requests
from pprint import pprint
from urllib.parse import urlencode, urlparse
import time
from itertools import chain


def list_div(list_for_split, n=25):
    return [list_for_split[i:i + n] for i in range(0, len(list_for_split), n)]

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.63'
APP_ID = 5863643
api_address = 'https://api.vk.com/method/'

# auth_data = {
#     'client_id': APP_ID,
#     'display': 'mobile',
#     'response_type': 'token',
#     'scope': 'friends,groups,status,offline',
#     'v': VERSION
# }

access_token = '76e01e83604e3f9e6527ab13fb0320d4cefd4fa8424a93c3f6032c1f94096f9d09b7fd1bcd0954a9b54db'
user_id = 1140044
params = {
    'user_id': user_id,
    'access_token': access_token,
    'v': VERSION
}

# получаем список друзей
friends_method = 'friends.get'
response1 = requests.get(api_address + friends_method, params)
friends_list = response1.json()['response']['items']
print(len(friends_list))

# получаем количество подписчиков
followers_method = 'users.getFollowers'
response2 = requests.get(api_address + followers_method, params)
followers_count = response2.json()['response']['count']

# получаем список подписчиков
all_followers = []
offset_parm = 0
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
print(all_followers)

divided_list = list_div(all_followers)

method = 'execute?access_token=' + access_token + '&code='

merge_list = []
for l in divided_list:
    code = 'return ['
    for user_id in l:
        code = '%s%s' % (code, 'API.groups.get({"user_id":%s}),' % str(user_id))
    code = '%s%s' % (code, '];')
    r = requests.get(api_address + method + code).json()['response']
    # time.sleep(.200)
    # print(r)
    for i in r:
        if type(i) == type(True):
            r.remove(i)
        else:
            merge_list.append(i)
print(merge_list)
full_merge_list = sum(merge_list, [])
print(full_merge_list)

