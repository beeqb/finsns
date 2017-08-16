#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2


URL = 'http://search.sina.com.cn/?c=news&q=%s&range=all&time=custom&stime=2013-12-01&etime=2017-08-17&num=20&col=1_7&page=%d'


def crawler(keyword, pg):
    url = URL % (urllib2.quote(keyword.decode('utf-8').encode('gbk')), pg)
    page = urllib2.urlopen(url).read()
    return page

def


def main():
    keyword = '浦发银行'
    page = crawler(keyword, 10)
    with open('test10.html', 'w') as f:
        f.write(page)


if __name__ == '__main__':
    main()
