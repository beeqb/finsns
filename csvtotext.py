# -*- coding: utf-8 -*-

import unicodecsv

STOCKS_FILE = 'shangzheng180.csv'


def get_stocks(f):
    csv_data = unicodecsv.reader(f, encoding='gbk')
    # csv_data = csv.reader(f, encoding='utf-8')
    stocks = []
    names = []
    for row in csv_data:
        stocks.append(row[0].encode('utf-8'))
        names.append(row[1].encode('utf-8'))
    return stocks, names


def main():
    with open(STOCKS_FILE, 'rb') as f:
        stocks, names = get_stocks(f)

    with open('shangzheng180utf8.csv', 'w') as f:
        for s, n in zip(stocks, names):
            f.write(s + ',' + n + '\n')

if __name__ == '__main__':
    main()
