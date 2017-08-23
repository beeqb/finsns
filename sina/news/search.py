#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import json



# URL = 'http://search.sina.com.cn/?c=news&q=%s&range=all&time=custom&stime=2013-12-01&etime=2017-08-17&num=20&col=1_7&page=%d'
# URL = 'http://api.search.sina.com.cn/?q=%s&range=all&c=news&time=custom&stime=%s&etime=%s&num=50&page=%d&col=1_7'
URL = 'http://api.search.sina.com.cn/?c=news&q=%s&range=all&time=custom&stime=%s&etime=%s&num=50&col=1_7&page=%d&from=dfz_api'
NUM_ITEMS = 50


def handle_exceptions(ef, url):
    ef.write(url + '\n')


def crawler(keyword, ef, stime, etime, pg):
    url = URL % (keyword, stime, etime, pg)

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
    # url = URL % (urllib2.quote(keyword.decode('utf-8').encode('gbk')), pg)
    return resp


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


def search_csv(name, stime, etime, writer, ef):
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
