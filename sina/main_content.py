# -*- coding: utf-8 -*-

from news.process import Finnews
#import unicodecsv as csv
import csv
import unicodecsv


STOCKS_FILE = '../shangzheng180.csv'
DATA_FILE = '../newscontents/%s.txt'
URLS_FILE = '../newsrecord/%s.csv'
SIZE = 1000


def get_stocks(f):
    csv_data = unicodecsv.reader(f, encoding='gbk')
    # csv_data = csv.reader(f, encoding='utf-8')
    stocks = []
    names = []
    for row in csv_data:
        stocks.append(row[0].encode('utf-8'))
        names.append(row[1].encode('utf-8'))
    return stocks, names


def get_contents(f, urls, kw, titles):
    n = len(urls) // 1000
    for i in range(n):
        si = i*1000
        ei = (i+1)*1000
        fns = Finnews(urls[si:ei])
        fns.start()
        print('Start to write contents: Part %d...' % (i))
        for j in range(si, ei):
            if kw in titles[j]:
                c = fns.get_content(j-i*1000)
            else:
                c = fns.get_keyword_content(j-i*1000, kw)
            if c == '':
                f.write(titles[j] + ': ' + urls[j])
            f.write(titles[j] + ':\n"' + c + '"')
            f.write('\n\n')
    if len(urls)-n*1000 > 0:
        si = len(urls)-n*1000
        fns = Finnews(urls[-si:])
        fns.start()
        for j in range(si):
            if kw in titles[len(urls)-si+j]:
                c = fns.get_content(j)
            else:
                c = fns.get_keyword_content(j, kw)
            f.write(titles[len(urls)-si+j] + ':\n"' + c + '"')
            f.write('\n\n')


def main():
    with open(STOCKS_FILE, 'rb') as f:
        stocks, names = get_stocks(f)

    ef = open('url_errors.txt', 'w')

    # for test only
    # stocks = ['600000']
    # names = ['浦发银行']

    for stock, name in zip(stocks, names):
        print('Start getting %s, %s:.....' % (stock, name))
        urls = []
        titles = []
        with open(URLS_FILE % stock, 'r') as f:
            csv_data = csv.reader(f)
            for row in csv_data:
                titles.append(row[0].strip('"'))
                urls.append(row[4].strip('"'))
        with open(DATA_FILE % stock, 'w') as f:
            get_contents(f, urls, name, titles)

    ef.close()

if __name__ == '__main__':
    main()
