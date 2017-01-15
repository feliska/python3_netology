import json


with open("cook_book.json", 'r') as cook:
    cook_book = json.load(cook)

    def get_shop_list_by_dishes(dishes, people_count):
        shop_list = {}
        for dish in dishes:
            for ingredient in dish['ingredients']:
                new_shop_item = dict(ingredient)
                # пересчитали ингрединты по количеству людей
                new_shop_item['quantity'] = new_shop_item['quantity'] * people_count
                if new_shop_item['product'] not in shop_list:
                    shop_list[new_shop_item['product']] = new_shop_item
                else:
                    shop_list[new_shop_item['product']]['quantity'] += new_shop_item['quantity']
        return shop_list


def print_shop_list(shop_list):
    for key, shop_list_item in shop_list.items():
        print("{product} {quantity} {unit}".format(**shop_list_item))


def create_shop_list(people_count, dishes):
    #заполнили список покупок
    shop_list = get_shop_list_by_dishes(dishes, people_count)
    # Вывести список покупок
    print_shop_list(shop_list)


dishes = []
print('Введите название блюда. Для окончания выбора введите "exit"')
while True:
    dish_select = input().lower()
    if dish_select == 'exit':
        break
    elif dish_select in cook_book:
        dishes.append(cook_book[dish_select])
    elif dish_select not in cook_book:
        print('Такого блюда нет в поваренной книге')


print('На сколько человек?')
people_count = int(input())

print('Список покупок: ')
create_shop_list(people_count, dishes)
