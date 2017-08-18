#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import unicodecsv as csv
import lxml.html


URL = 'http://search.sina.com.cn/?c=news&q=%s&range=all&time=custom&stime=2013-12-01&etime=2017-08-17&num=20&col=1_7&page=%d'
STOCKS_FILE = 'shangzheng180.csv'


def get_stocks(f):
#    csv_data = csv.reader(f, encoding='gbk')
    csv_data = csv.reader(f, encoding='utf-8')
    stocks = []
    names = []
    for row in csv_data:
        stocks.append(row[0])
        names.append(row[1])
    return stocks, names


def crawler(keyword, pg):
#    url = URL % (urllib2.quote(keyword.encode('gbk')), pg)
    url = URL % (urllib2.quote(keyword.decode('utf-8').encode('gbk')), pg)
    page = urllib2.urlopen(url).read()
    return page


def process_page(page, pg):
#    content = lxml.html.fromstring(page).getroot()
    with open('test.html', 'w') as f:
        f.write(page)
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
        titles.append(title_link.text_content())
        meta = header.cssselect('span')[0].text_content().split(' ')
        sources.append(meta[0])
        dates.append(meta[1])
        times.append(meta[2])
        url = title_link.get('href')
        contents.append(get_content(url))
    if pg == 1:
        return total_num, titles, dates, times, sources, contents
    else:
        return titles, dates, times, sources, contents


def get_content(url):
    page = urllib2.urlopen(url).read()
    dom_page = lxml.html.fromstring(page).getroot()
    content = dom_page.cssselect('div#artibody')
    if not content:
        return url
    article = []
    for p in content.cssselect('p'):
        article.append(p.text_content())
    return article


def main():
    with open(STOCKS_FILE, 'rb') as f:
        stocks, names = get_stocks(f)
    page = crawler(names[0], 1)
    total_num, titles, dates, times, sources, contents = process_page(page, 1)
    print total_num
    with open('%d' % stocks[0], 'wb') as f:
        writer = csv.writer(f)
        for title, date, time, source, content in zip(titles, dates, times, sources, contents):
            writer.writerow(title, date, time, source, content)
    # for stock, name in zip(stocks, names):
    #     page = crawler(name, 1)
    #     with open('test10.html', 'w') as f:
    #         f.write(page)


if __name__ == '__main__':
    main()
