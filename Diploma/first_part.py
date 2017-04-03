import requests
from pprint import pprint
from urllib.parse import urlencode, urlparse
import time
import vk

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

followers_method = 'users.getFollowers'
response2 = requests.get(api_address + followers_method, params)
followers_count = response2.json()['response']['count']

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

print(followers_count)
print(len(all_followers))

# print(len(followers_list))

group_method = 'groups.get'
all_groups = []
n = 0
user_id = str(user_id)
for user_id in friends_list:
    r = requests.get('https://api.vk.com/method/execute?access_token=' + access_token + '&code=return API.groups.get({"user_id":"'+ str(user_id) +'","count":"3"});')
    print(r.json())
# for user_id in friends_list:
#     params = {
#         'user_id': user_id,
#         'access_token': access_token,
#         'v': VERSION,
#         'count': "1"
#     }
#     # '&code=return API.wall.get({"owner_id":"' + owner_id + '","count":"1"});'
#     response2 = requests.get(api_address + group_method, params)
#     group_list = response2.json()['response']['items']
#     n += 1
#     print(n)
#     all_groups.extend(group_list)
#     print(all_groups)
#     time.sleep(.200)


# user_group = vkapi('groups.get', user_id=1140044)
# print(user_group)
# for user_id in friends_list:
#
#
#     print(user_id)
#     print(user_group)
