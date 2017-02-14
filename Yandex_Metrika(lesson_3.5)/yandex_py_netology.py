from urllib.parse import urlencode, urlparse, urljoin
from pprint import pprint
import requests

autorize_url = 'https://oauth.yandex.ru/authorize'
app_id = 'fa70f6b343a049a6a920e342c4a1f3a1'

auth_data = {
    'response_type': 'token',
    'client_id': app_id
}

# print('?'.join((autorize_url, urlencode(auth_data))))

TOKEN = 'AQAAAAAO7hI3AAQPo12_zUyJokYGnWdPljlpEKs'