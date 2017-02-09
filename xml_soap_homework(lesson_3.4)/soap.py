import osa
import re
import math

# компиляция регулярных выражений
t_exp = re.compile('\D')
c_exp = re.compile('\s')


def temps_convert(temp):
    # функция для конвертации температур
    url = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
    client = osa.Client(url)
    response = client.service.ConvertTemp(Temperature=temp, FromUnit='degreeFahrenheit', ToUnit='degreeCelsius')
    return response


def length_convert(length):
    # функция для конвертации мер длины
    url = 'http://www.webservicex.net/length.asmx?WSDL'
    client = osa.Client(url)
    response = client.service.ChangeLengthUnit(LengthValue=length, fromLengthUnit='Miles', toLengthUnit='Kilometers')
    return response


def currency_convert(val, cur_name):
    # функция для конвертации валют
    url = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
    client = osa.Client(url)
    response = client.service.ConvertToNum(fromCurrency=cur_name, toCurrency='RUB', amount=val, rounding=True)
    return response


def get_temps(file_name):
    # получение списка температур, расчет среднего арифм. и конвертация
    temps = []
    with open(file_name) as t:
        a = t.readlines()
        for i in a:
            a_clean = t_exp.sub('', i)
            temps.append(int(a_clean))
    return temps_convert(sum(temps)/len(temps))


def get_money_amounts(file_name):
    # получение сумм, конвертация и округление до большего целого
    money_amount = []
    with open(file_name) as c:
        all_val = c.readlines()
        for i in all_val:
            cur_string = i.split(' ')
            tots = currency_convert(cur_string[1], c_exp.sub('', cur_string[2]))
            money_amount.append(tots)
    return math.ceil(sum(money_amount))


def get_length(file_name):
    # получение из файла расстояний, конвертирование, округление
    lengths = []
    with open(file_name) as l:
        all_len = l.readlines()
        for i in all_len:
            len_string = i.split(' ')
            lengths.append(float(len_string[1].replace(',', '')))
    return round(length_convert(sum(lengths)), 2)


print("Средняя арифметическая температура по Цельсию:", get_temps('temps.txt'))
print("Суммарное расстояние пути в километрах:", get_length('travel.txt'))
print("Сумма всех затрат на путешествие:", get_money_amounts('currencies.txt'))
