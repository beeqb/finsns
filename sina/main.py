#!/usr/bin/env python
# -*- coding: utf-8 -*-

from news.search import search_csv
from news.content import gcrawler
from news.process import Finnews
import unicodecsv as csv


STOCKS_FILE = '../shangzheng180.csv'


def get_stocks(f):
    csv_data = csv.reader(f, encoding='gbk')
    # csv_data = csv.reader(f, encoding='utf-8')
    stocks = []
    names = []
    for row in csv_data:
        stocks.append(row[0].encode('utf-8'))
        names.append(row[1].encode('utf-8'))
    return stocks, names


def gen_time():
    years = [i for i in range(2013, 2018)]
    months = [i for i in range(1, 13)]
    stime = []
    etime = []
    for y in years:
        for m in months:
            stime.append('%d-%d-1' % (y, m))
            etime.append('%d-%d-31' % (y, m))
    return stime, etime


def main():
    with open(STOCKS_FILE, 'rb') as f:
        stocks, names = get_stocks(f)

    stime, etime = gen_time()
    ef = open('url_errors.txt', 'w')

    for stock, name in zip(stocks, names):
        print 'Start getting %s, %s:.....' % (stock, name)
        with open('%s.csv' % stock, 'wb') as f:
            writer = csv.writer(f)
            search_csv(name, stime, etime, writer, ef)

    ef.close()

if __name__ == '__main__':
    main()
