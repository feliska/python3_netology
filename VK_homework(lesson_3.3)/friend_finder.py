from pprint import pprint
from urllib.parse import urlencode, urlparse
import requests


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

token_url = 'https://oauth.vk.com/blank.html#access_token=11b48fd7a39975d1ff59d81e33406307a678e697c508eeb7e13cdb66d94d5b1e4dee13d12866c04ec4640&expires_in=86400&user_id=1140044'

o = urlparse(token_url)
fragments = dict((i.split('=') for i in o.fragment.split('&')))
access_token = fragments['access_token']
# print(access_token)

params = {
    'access_token': access_token,
    'v': VERSION
}
# получение списка друзей
method = 'friends.get'
response1 = requests.get(api_address + method, params)
friends_list = response1.json()['response']['items']
print(friends_list)

for user_id in friends_list:
    user = requests.get(api_address+'users.get', {'user_id': user_id})
    response = requests.get(api_address+method, {'user_id': user_id})
    print(user.json(), response.json())
