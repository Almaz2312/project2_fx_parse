import csv

import requests
from bs4 import BeautifulSoup
import datetime


#Получаем данные в случае статуса кода 200
def get_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "Error"


# Записываем стягиваемые данные в таблицу
def get_fx(html):
    list_ = []
    table = []
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="col-md-9")
    fxtable = content.find("table", {"id" : "rates_table"})
    fxdata = fxtable.find_all('tr')
    """
        Получаем данные курсов банка и названия банка из тега "tr"
        и проходимся по данным через for, а получаемый результат
        записываем в список - table
    """
    for data in fxdata:
        lt = data.get_text(separator=";").replace(',', '.').split(';')
        table.append(lt)
    for f in table[0]:
        list_.append(f)
        list_.append(f)
    """
    Доавляем заголок через таблицу f и дублируем их названия.
    Т.к нужно дублировать заголовки со второй, то здесь после записи
    удаляется первый из списка f. После удаляется первый индекс из списка table,
    т.к это не дублированный заголовок и вставляется дублированный заголок. 
    """
    list_.remove(list_[0])
    table.remove(table[0])
    table.insert(0, list_)
    return table


# Создаём csv файл на основе функции get_fx
def make_csv(tables):
    now = datetime.datetime.now()

    with open(f'fxrates{now}.csv', "w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        """
        Добавляем верзние поля и записываем данные через for в csv файл
        """
        for table in tables:
            writer.writerow(table)


# Запускаем наши функции из функции main()
def main():
    URL = "https://www.akchabar.kg/ru/exchange-rates/"
    print(__name__)
    response = get_response(URL)
    fx_data = get_fx(response)
    print(fx_data)
    make_csv(fx_data)


# Запускаем функцию main()
if __name__ == "__main__":
    main()