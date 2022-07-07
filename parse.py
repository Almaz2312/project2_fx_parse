import csv

import requests
from bs4 import BeautifulSoup


#Получаем данные в случае статуса кода 200
def get_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "Error"


# Записываем стягиваемые данные в таблицу
def get_fx(html):
    table = []
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="col-md-9")
    fxtable = content.find("table", {"id" : "rates_table"})
    thr = fxtable.find("tbody")
    fxdata = thr.find_all('tr')
    """
        Получаем данные курсов банка и названия банка из тега "tr"
        и проходимся по данным через for, а получаемый результат
        записываем в список - table
    """
    for data in fxdata:
        lt = data.get_text(separator=";").replace(',', '.').split(';')
        table.append(lt)
    return table


# Создаём csv файл на основе функции get_fx
def make_csv(tables):
    with open('fxrates.csv', "w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        """
        Добавляем верзние поля и записываем данные через for в csv файл
        """
        writer.writerow(['Банки', 'Покупка USD', 'Продажа USD',
                         'Покупка EUR','Продажа EUR',
                         'Покупка RUB', 'Продажа RUB',
                         'Покупка KZT', 'Продажа KZT'])
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