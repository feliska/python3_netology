with open('cook_book.txt') as cookbook:
    cook_book = {}
    for line in cookbook:
        ingredients = []
        dish = line.lower().strip()
        ingredients_count = int(cookbook.readline())
        cook_book[dish] = {'ingredients': ingredients}

        for count in range(ingredients_count):
            # использование 2х replace подряд смущает немного
            ingredients_of_dish = list(map(str, cookbook.readline().replace("\n", '').replace(" ", '').split('|')))
            includes = {
                'product': ingredients_of_dish[0],
                'quantity': int(ingredients_of_dish[1]),
                'unit': ingredients_of_dish[2]
            }
            ingredients.append(includes)

        blank_line = cookbook.readline()


    print(cook_book)

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

def create_shop_list(people_count, first_dish, second_dish, third_dish):
    # получить блюда из кулинарной книги
    dish1 = cook_book[first_dish]
    dish2 = cook_book[second_dish]
    dish3 = cook_book[third_dish]
    dishes = [dish1, dish2, dish3]
    #заполнили список покупок
    shop_list = get_shop_list_by_dishes(dishes, people_count)
    # Вывести список покупок
    print_shop_list(shop_list)

print('Выберите первое блюдо: ')
first_dish = input().lower()
print('Выберите второе блюдо: ')
second_dish = input().lower()
print('Выберите третье блюдо: ')
third_dish = input().lower()
print('На сколько человек?')
people_count = int(input())

print('Список покупок: ')
create_shop_list(people_count, first_dish, second_dish, third_dish)