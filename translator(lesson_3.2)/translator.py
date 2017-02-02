import requests
import glob

files = glob.glob('*.txt')

KEY = 'trnsl.1.1.20170201T000148Z.30f56ecf5eefa4f9.88a2f27402be4be7eaf0df0ed5fa88be76f65cf4'
lang_out = 'ru'


def lang_name(lang_code):
    # определение языка по буквенному коду
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs'
    params = {
        'key': KEY,
        'ui': lang_code
    }
    response = requests.get(URL, params=params)
    data = response.json()
    lang = data['langs'][lang_code]
    return lang


def translate_to_ru(text, lang_code, lang_to_translate):
    # перевод текста на русский язык (по умолчанию)
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': KEY,
        'text': text,
        'lang': lang_code + '-' + lang_to_translate
    }
    response = requests.get(URL, params=params)
    data = response.json()
    translated = data['text']
    translated = ' '.join(translated)
    return translated


def detect_lang(text):
    # функция определения языка, его кода
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    params = {
        'key': KEY,
        'text': text
    }
    response = requests.get(URL, params=params)
    data = response.json()
    d_lang = str(data['lang'])
    return d_lang


def file_translate(file_name):
    # перевод текста в файлах .txt, содержащихся в исходной папке
    for file_name in files:
        with open(file_name) as f:
            text_for_translate = f.read()
            print("Переводится:", file_name)
            language = detect_lang(text_for_translate)
            fst_str = "Язык перевода: " + lang_name(language)+'\n'
            scd_str = translate_to_ru(text_for_translate, language, lang_out)
            with open('translated_'+file_name, 'w') as t:
                t.write(fst_str)
                t.write(scd_str)


file_translate(files)
