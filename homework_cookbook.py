import re

# компиляция выражения для удаления лишних пробельных символов
reg = re.compile('^\s|\s$')

with open('cook_book.txt') as cookbook:
    cook_book = {}
    for line in cookbook:
        ingredients = []
        dish = line.lower().strip()
        ingredients_count = int(cookbook.readline())
        cook_book[dish] = {'ingredients': ingredients}

        for count in range(ingredients_count):
            ingr_line = cookbook.readline().split('|')
            ingredients_of_dish = []
            # заменила 2 реплейса на цикл с удалением ненужных знаков по регулярке
            for i in ingr_line:
                ingr = reg.sub('', i)
                ingredients_of_dish.append(ingr)
            includes = {
                'product': ingredients_of_dish[0],
                'quantity': int(ingredients_of_dish[1]),
                'unit': ingredients_of_dish[2]
            }
            ingredients.append(includes)

        blank_line = cookbook.readline()


def get_shop_list_by_dishes(dishes, people_count):
    shop_list = {}
    for dish in dishes:
        for ingridient in dish['ingredients']:
            new_shop_item = dict(ingridient)
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