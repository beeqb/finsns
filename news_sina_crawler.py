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
    url = URL % (keyword, stime, etime, pg)
#    url = URL % (urllib2.quote(keyword.decode('utf-8').encode('gbk')), pg)
    resp = urllib2.urlopen(url).read()
    return resp


def process_page(resp, pg):
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
        return total_num, titles, dates, times, sources, contents
    else:
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


def main():
    with open(STOCKS_FILE, 'rb') as f:
        stocks, names = get_stocks(f)

    for stock, name in zip(stocks, names):
        print 'Start getting %s:.....' % (stock.encode('gbk'))
        with open('%s.csv' % stock.encode('gbk'), 'wb') as f:
            writer = csv.writer(f)
            page = crawler(name, 1)
            total_num, titles, dates, times, sources, contents = process_page(page, 1)
            print total_num
            for title, date, time, source, content in zip(titles, dates, times, sources, contents):
                writer.writerow([title, date, time, source, content])
            if total_num > 20:
                total_page = total_num / NUM_ITEMS + (total_num % NUM_ITEMS > 0)
                for i in xrange(2, total_page+1):
                    titles, dates, times, sources, contents = process_page(page, i)
                    for title, date, time, source, content in zip(titles, dates, times, sources, contents):
                        writer.writerow([title, date, time, source, content])


if __name__ == '__main__':
    main()
