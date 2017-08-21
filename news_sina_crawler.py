#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import unicodecsv as csv
import json
from bs4 import BeautifulSoup


# URL = 'http://search.sina.com.cn/?c=news&q=%s&range=all&time=custom&stime=2013-12-01&etime=2017-08-17&num=20&col=1_7&page=%d'
# URL = 'http://api.search.sina.com.cn/?q=%s&range=all&c=news&time=custom&stime=%s&etime=%s&num=50&page=%d&col=1_7'
URL = 'http://api.search.sina.com.cn/?c=news&q=%s&range=all&time=custom&stime=%s&etime=%s&num=50&col=1_7&page=%d&from=dfz_api'
STOCKS_FILE = 'shangzheng180.csv'
NUM_ITEMS = 50


def get_stocks(f):
    csv_data = csv.reader(f, encoding='gbk')
#    csv_data = csv.reader(f, encoding='utf-8')
    stocks = []
    names = []
    for row in csv_data:
        stocks.append(row[0])
        names.append(row[1])
    return stocks, names


def crawler(keyword, stime, etime, pg):
    url = URL % (urllib2.quote(keyword), stime, etime, pg)
#    url = URL % (urllib2.quote(keyword.decode('utf-8').encode('gbk')), pg)
    resp = urllib2.urlopen(url).read()
    return resp


def process_resp(resp, pg):
    content = (json.loads(resp))['result']
    if pg == 1:
        total_num = int(content['count'])
    titles = []
    dates = []
    times = []
    sources = []
    contents = []
    for item in content['list']:
        titles.append(item['title'])
        sources.append(item['media'])
        dates.append(item['datetime'].split(' ')[0])
        times.append(item['datetime'].split(' ')[1])
        url = item['url']
        contents.append(get_content(url))
    if pg == 1:
        print total_num

    return titles, dates, times, sources, contents


def get_content(url):
    try:
        page = urllib2.urlopen(url).read()
    except urllib2.URLError:
        print url
        return url
    dom_page = BeautifulSoup(page, 'html.parser')
    content = dom_page.select('div#artibody')
    if not content:
        return url
    article = []
    for p in content[0].select('p'):
        article.append(p.get_text())
    return ''.join(article)


def gen_time():
    years = [i for i in range(2013, 2018)]
    months = [i for i in range(1, 13)]
    stime = ['%d-%d-1' % (i, j) for i, j in zip(years, months)]
    etime = ['%d-%d-31' % (i, j) for i, j in zip(years, months)]
    return stime, etime


def start_crawler(name, stime, etime, writer):
    for s, e in zip(stime, etime):
        is_end = 0
        is_retry = 0
        n_page = 1

        while not is_end:
            resp = crawler(name, s, e, n_page)
            titles, dates, times, sources, contents = process_resp(resp, n_page)
            if not titles:
                if is_retry:
                    is_end = 1
                else:
                    is_retry = 1
                    continue
            if is_retry:
                is_retry = 0
            for title, date, time, source, content in zip(titles, dates, times, sources, contents):
                writer.writerow([title, date, time, source, content])
                n_page = n_page + 1


def main():
    with open(STOCKS_FILE, 'rb') as f:
        stocks, names = get_stocks(f)

    stime, etime = gen_time()

    for stock, name in zip(stocks, names):
        print 'Start getting %s:.....' % (stock.encode('gbk'))
        with open('%s.csv' % stock.encode('gbk'), 'wb') as f:
            writer = csv.writer(f)
            start_crawler(name, stime, etime, writer)

if __name__ == '__main__':
    main()
