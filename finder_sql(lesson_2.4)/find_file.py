import glob
import os.path

migrations = 'Migrations'

files = glob.glob(os.path.join(migrations, "*.sql"))

files_list = []


def first_search(file_list, second_file_list, search_parameter):
    for file in file_list:
        with open(file) as f:
            where_to_find = f.read()
            s = where_to_find.find(search_parameter)
            if s != -1:
                print(file)
                second_file_list.append(file)
    print("Всего:", len(second_file_list))
    file_list.clear()


def second_search(file_list, second_file_list, search_parameter):
    for file in second_file_list:
        with open(file) as f:
            where_to_find = f.read()
            s = where_to_find.find(search_parameter)
            if s != -1:
                print(file)
                file_list.append(file)
    print("Всего:", len(file_list))
    second_file_list.clear()


def search_input():
    print("Введите строку:")
    search = input()
    return search


while True:
    first_search(files, files_list, search_input())
    second_search(files, files_list, search_input())

