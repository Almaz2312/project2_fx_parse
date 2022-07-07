import csv

import requests
from bs4 import BeautifulSoup


def get_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "Error"


def get_fx(html):
    table = []
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="col-md-9")
    fxtable = content.find("table", {"id" : "rates_table"})
    thr = fxtable.find("tbody")
    fxdata = thr.find_all('tr')
    for data in fxdata:
        lt = data.get_text(separator=";").replace(',', '.').split(';')
        table.append(lt)
    return table


def make_csv(tables):
    chars = ('[', ']')
    new = ' '
    with open('fxrates.csv', "w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Банки', 'Покупка USD', 'Продажа USD',
                         'Покупка EUR','Продажа EUR',
                         'Покупка RUB', 'Продажа RUB',
                         'Покупка KZT', 'Продажа KZT'])
        for table in tables:
            writer.writerow(table)


def main():
    URL = "https://www.akchabar.kg/ru/exchange-rates/"
    print(__name__)
    response = get_response(URL)
    fx_data = get_fx(response)
    print(fx_data)
    make_csv(fx_data)


if __name__ == "__main__":
    main()