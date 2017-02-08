from pprint import pprint
from urllib.parse import urlencode, urlparse
import requests


def parts(list_of_friends, n=100):
    return [list_of_friends[i:i + n] for i in range(0, len(list_of_friends), n)]


AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.62'
APP_ID = 5863643
api_address = 'https://api.vk.com/method/'

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'response_type': 'token',
    'scope': 'friends,status',
    'v': VERSION
}

# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

# token_url = 'https://oauth.vk.com/blank.html#access_token=8e777ca1a0e6ad8571680ecc565299519cf9c4ed9f0c7eec245e024706e00d50e2aab1c5f965644f891f1&expires_in=86400&user_id=1140044'
# # token_url = 'https://oauth.vk.com/blank.html#access_token=11b48fd7a39975d1ff59d81e33406307a678e697c508eeb7e13cdb66d94d5b1e4dee13d12866c04ec4640&expires_in=86400&user_id=1140044'
#
# o = urlparse(token_url)
# fragments = dict((i.split('=') for i in o.fragment.split('&')))
# access_token = fragments['access_token']
# print(access_token)
access_token = '8e777ca1a0e6ad8571680ecc565299519cf9c4ed9f0c7eec245e024706e00d50e2aab1c5f965644f891f1'

my_user_id = 1140044
params = {
    'access_token': access_token,
    'v': VERSION
}
# получение списка друзей
method1 = 'friends.get'

response1 = requests.get(api_address + method1, params)
my_friends_list = response1.json()['response']['items']
# получение списка друзей друзей
for user_id in my_friends_list:
    response2 = requests.get(api_address + method1, {'user_id': user_id})
    print({user_id: response2.json()['response']})

# поиск общих друзей
method2 = 'friends.getMutual'

for i in parts(my_friends_list):
    target_uids_list = ', '.join(map(str, i))
    params = {
        'access_token': access_token,
        'source_uid': my_user_id,
        'target_uids': target_uids_list,
        'v': VERSION
    }

    response3 = requests.get(api_address + method2, params)
    print(target_uids_list)
    pprint(response3.json())




