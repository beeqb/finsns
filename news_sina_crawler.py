#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import unicodecsv as csv
import lxml.html
from bs4 import BeautifulSoup


# URL = 'http://search.sina.com.cn/?c=news&q=%s&range=all&time=custom&stime=2013-12-01&etime=2017-08-17&num=20&col=1_7&page=%d'
URL = 'http://api.search.sina.com.cn/?q=%E6%B5%A6%E5%8F%91%E9%93%B6%E8%A1%8C&range=all&c=news&sort=time&ie=utf-8&from=dfz_api&time=custom&stime=2013-12-01&etime=2013-12-31&num=20&page=1&col=1_7'
STOCKS_FILE = 'shangzheng180.csv'
NUM_ITEMS = 20


def get_stocks(f):
    csv_data = csv.reader(f, encoding='gbk')
#    csv_data = csv.reader(f, encoding='utf-8')
    stocks = []
    names = []
    for row in csv_data:
        stocks.append(row[0])
        names.append(row[1])
    return stocks, names


def crawler(keyword, pg):
    url = URL % (urllib2.quote(keyword.encode('gbk')), pg)
#    url = URL % (urllib2.quote(keyword.decode('utf-8').encode('gbk')), pg)
    page = urllib2.urlopen(url).read()
    return page


def process_page(page, pg):
    content = lxml.html.fromstring(page)
    if pg == 1:
        t = content.cssselect('div#result div.l_v2')[0].text_content()
        total_num = int(''.join([s for s in t if s.isdigit()]))
    items = content.cssselect('div#result div.box-result')
    titles = []
    dates = []
    times = []
    sources = []
    contents = []
    for item in items:
        header = item.cssselect('h2')[0]
        title_link = header.cssselect('a')[0]
        titles.append(title_link.text_content().encode('utf-8'))
        meta = header.cssselect('span.fgray_time')[0].text_content().split(' ')
        sources.append(meta[0].encode('utf-8'))
        dates.append(meta[1].encode('utf-8'))
        times.append(meta[2].encode('utf-8'))
        url = title_link.get('href')
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
