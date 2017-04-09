import requests
import json
import time
from collections import Counter


# деление списка на части
def list_div(list_for_split, n=25):
    return [list_for_split[i:i + n] for i in range(0, len(list_for_split), n)]


# получение списка друзей по id
def friends_get(id_of_user):
    params['user_id'] = id_of_user
    response = requests.get(api_address + 'friends.get', params)
    try:
        friends_list = response.json()['response']['items']
        print("Количество друзей:", len(friends_list))
    except KeyError:
        friends_list = []
        print("Список друзей закрыт")
    return all_followers.extend(friends_list)


# получение количества подписчиков и их списка
def followers_get(id_of_user):
    params['user_id'] = id_of_user
    params['count'] = 1000
    response = requests.get(api_address + 'users.getFollowers', params).json()
    followers_count = response['response']['count']
    print("Общее количество подписчиков:", followers_count)
    followers_list = response['response']['items']
    all_followers.extend(followers_list)
    return all_followers


# получение списков групп подписчиков
def get_followers_groups(full_list_of_users):
    divided_list = list_div(full_list_of_users)
    all_followers_count = len(full_list_of_users)
    merge_list = []
    user_count = 0
    method = 'execute?access_token=' + access_token + '&code='
    print("Обработка групп, в которых состоят подписчики ...")
    for l in divided_list:
        code = 'return ['
        user_count += 25
        remain_to_calc = all_followers_count - user_count
        if remain_to_calc > 0:
            print("Осталось обработать %s из %s подписчиков" % (remain_to_calc, all_followers_count))
        else:
            print("Обработка почти завершена =))", end='\n')
        for user in l:
            code = '%s%s' % (code, 'API.groups.get({"user_id":%s}),' % str(user))
        code = '%s%s' % (code, '];')
        r = requests.get(api_address + method + code).json()['response']
        for i in r:
            if type(i) == type(True):
                r.remove(i)
            else:
                merge_list.append(i)
    groups = Counter(sum(merge_list, [])).most_common(100)
    return groups


# запрос названия групп и формирование списка для выгрузки в json
def top_groups(counted_groups):
    top_groups_list = []
    print("Топ 100 групп, в которых состоят подписчики:", end='\n')
    for group, k in counted_groups:
        params['group_id'] = group
        name = requests.get(api_address + 'groups.getById', params).json()['response'][0]['name']
        print(name, k)
        a = {'title': name, 'count': k, 'id': group}
        top_groups_list.append(a)
        time.sleep(.200)
    return top_groups_list


# выгрузка топ 100 групп в файл
def top_100_file(id_of_user):
    friends_get(id_of_user)
    counted_groups = get_followers_groups(followers_get(id_of_user))
    top_100 = json.dumps(top_groups(counted_groups), ensure_ascii=False)
    print('\n'"Формирование файла top100.json", )
    with open("top100.json", 'w') as t:
        t.write(top_100)


version = '5.63'
api_address = 'https://api.vk.com/method/'
access_token = '76e01e83604e3f9e6527ab13fb0320d4cefd4fa8424a93c3f6032c1f94096f9d09b7fd1bcd0954a9b54db'
params = {
    'access_token': access_token,
    'v': version
}
all_followers = []
print("Введите id интересующей личности:")
user_id = input()

top_100_file(user_id)

