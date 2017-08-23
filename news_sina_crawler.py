#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import unicodecsv as csv
import json
from bs4 import BeautifulSoup
import cchardet as chardet
import grequests


# URL = 'http://search.sina.com.cn/?c=news&q=%s&range=all&time=custom&stime=2013-12-01&etime=2017-08-17&num=20&col=1_7&page=%d'
# URL = 'http://api.search.sina.com.cn/?q=%s&range=all&c=news&time=custom&stime=%s&etime=%s&num=50&page=%d&col=1_7'
URL = 'http://api.search.sina.com.cn/?c=news&q=%s&range=all&time=custom&stime=%s&etime=%s&num=50&col=1_7&page=%d&from=dfz_api'
STOCKS_FILE = 'shangzheng180.csv'
NUM_ITEMS = 50


def get_stocks(f):
    csv_data = csv.reader(f, encoding='gbk')
    # csv_data = csv.reader(f, encoding='utf-8')
    stocks = []
    names = []
    for row in csv_data:
        stocks.append(row[0].encode('utf-8'))
        names.append(row[1].encode('utf-8'))
    return stocks, names


def handle_exceptions(ef, url):
    ef.write(url + '\n')


def crawler(keyword, ef, **kargs):
    if not kargs:
        url = keyword
    else:
        url = URL % (keyword, kargs['stime'], kargs['etime'], kargs['pg'])
    retry = 0
    while retry < 3:
        try:
            resp = urllib2.urlopen(url).read()
            break
        except:
            retry = retry + 1
    if retry == 3:
        print url
        handle_exceptions(ef, url)
        return 0
#    url = URL % (urllib2.quote(keyword.decode('utf-8').encode('gbk')), pg)
    return resp


def gcrawler(urls, ef):
    rs = (grequests.get(u) for u in urls)
    return grequests.map(rs)


def process_resp(resp, pg, ef):
    content = (json.loads(resp))['result']
    if pg == 1:
        total_num = int(content['count'])
        print content['q'], content['page'], total_num
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
        # contents.append(get_content(url, ef))
        contents.append(url)

    return titles, dates, times, sources, contents


def get_content(url, ef):
    page = crawler(url, ef)
    if page == 0:
        return url
    dom_page = BeautifulSoup(page, 'html.parser')
    content = dom_page.select('div#artibody')
    if not content:
        return url
    article = []
    for p in content[0].select('p'):
        article.append(p.get_text())
    return ''.join(article)


def gget_content(urls):
    resps = gcrawler(urls)
    contents = []
    for r, u in zip(resps, urls):
        if not r:
            contents.append(u)
        else:
            r.encoding = 'utf-8'
            page = r.text
            dom_page = BeautifulSoup(page, 'html.parser')
            content = dom_page.select('div#artibody')
            if not content:
                return u
            article = []
            for p in content[0].select('p'):
                article.append(p.get_text())
            return ''.join(article)


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


def start_crawler(name, stime, etime, writer, ef):
    for s, e in zip(stime, etime):
        is_end = 0
        is_retry = 0
        n_page = 1

        while not is_end:
            resp = crawler(name, ef, stime=s, etime=e, pg=n_page)
            if resp == 0:
                n_page = n_page + 1
                continue
            titles, dates, times, sources, contents = process_resp(resp, n_page, ef)
            if not titles:
                if is_retry:
                    is_end = 1
                    continue
                else:
                    is_retry = 1
                    continue
            if is_retry:
                is_retry = 0
            for title, date, time, source, content in zip(titles, dates, times, sources, contents):
                writer.writerow(['"%s"' % title,
                                 date, time,
                                 source,
                                 '"%s"' % content])
            n_page = n_page + 1


def main():
    with open(STOCKS_FILE, 'rb') as f:
        stocks, names = get_stocks(f)

    stime, etime = gen_time()
    ef = open('url_errors.txt', 'w')

    for stock, name in zip(stocks, names):
        print 'Start getting %s, %s:.....' % (stock, name)
        with open('%s.csv' % stock, 'wb') as f:
            writer = csv.writer(f)
            start_crawler(name, stime, etime, writer, ef)

    ef.close()

if __name__ == '__main__':
    main()
