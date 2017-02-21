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


class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    token = None

    def __init__(self, token):
        self.token = token

    def get_header(self):
        return {
            'Content-Type': 'application/x-yametrika+json',
            'Authorization': 'OAuth {}'.format(self.token),
            'User-Agent': 'Chrome'
        }

    @property
    def counter_list(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        counter_list = [c['id'] for c in response.json()['counters']]
        return counter_list

    def get_visits_count(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': ['ym:s:visits', 'ym:s:pageviews', 'ym:s:users']
        }
        response = requests.get(url, params, headers=headers)
        visits_count = int(response.json()['data'][0]['metrics'][0])
        view_count = int(response.json()['data'][0]['metrics'][1])
        user_count = int(response.json()['data'][0]['metrics'][2])
        print("Количество визитов - {}, просмотров - {}, уникальных поситителей - {}".format(visits_count, view_count, user_count))
        # return visits_count, view_count, user_count



metrika = YandexMetrika(TOKEN)

print("Данные для счетчиков:", metrika.counter_list)

for counter in metrika.counter_list:
    metrika.get_visits_count(counter)

