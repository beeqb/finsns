 # -*- coding: utf-8 -*-

import time
import re
from functools import *
from crawler import gcrawler
from bs4 import BeautifulSoup


URL1 = 'http://guba.eastmoney.com/list,%s_1.html'
URL2 = 'http://guba.eastmoney.com/list,%s_2.html'
TIEZI_URL = 'http://guba.eastmoney.com/'

tiezi_list = {}

def get_codes(cf):
    return list(map(lambda x: x.rstrip(), cf.readlines()))


def   init_tiezi_set(code):
    urls = [URL1%(code), URL2%(code)]
    resps = gcrawler(urls)
    try:
        list_pages = list(map(lambda x: BeautifulSoup(x.text, 'html.parser'), resps))
    except:
        print(urls)
    tiezi_urls = extract_list_pages(list_pages)
    return tiezi_urls


def update_tiezi_set(code):
    gp_tiezi_set = tiezi_list[code]
    urls = [URL1%(code)]
    resps = gcrawler(urls)
    try:
        list_pages = list(map(lambda x: BeautifulSoup(x.text, 'html.parser'), resps))
    except:
        print(urls)
    new_tiezi_urls = extract_list_pages(list_pages)
    gp_tiezi_set.update(new_tiezi_urls)
    tiezi_list[code] = gp_tiezi_set


def extract_list_pages(list_pages):
    tiezi_doms = list(map(lambda x: x.select('div#articlelistnew div.articleh'), list_pages))
    tiezi_list = reduce(lambda x, y: x+y, tiezi_doms)
    tiezi_urls = []
    gp_tiezi_ids = []
    for x in tiezi_list:
        url_doms = x.select('span.l3 a')
        if not url_doms:
            continue
        url = url_doms[0]['href']
        if 'http' in url:
            continue
        if '/' in url:
            url = url[1:]
        tiezi_urls.append(TIEZI_URL+url)
        
    return set(tiezi_urls)


def get_yueping(urls):
    resps = gcrawler(urls)
    tiezis = []
    for x in resps:
        x.encoding = 'utf-8'
        tiezis.append(BeautifulSoup(x.text, 'html.parser'))
    yuedus = []
    pingluns = []
    titles = []
    for t in tiezis:
        zhuanping_doms = t.select('div#zwlist script')
        try:
            zhuanping_content = reduce(lambda x,y: x.text+y.text, zhuanping_doms)
        except:
            continue
        yuedu = re.search('var num=(.*?);.*', zhuanping_content).group(1)
        pinglun_pattern =  re.compile('.*var pinglun_num=(.*?);.*', re.S)
        pinglun= re.search(pinglun_pattern, zhuanping_content).group(1)
        title = t.select('div#zwconttbt')[0].text
        yuedus.append(yuedu)
        pingluns.append(pinglun)
        titles.append(title.strip())

    return (titles, yuedus, pingluns)


def writecsv(tiezi_urls, titles, yuedus, pingluns, wf):
        ttime=time.strftime("%Y-%m-%d %H:%M", time.localtime())
        for t_url, t, y, p in zip(tiezi_urls, titles, yuedus, pingluns):
            t_id = (t_url.split(',')[2]).split('.')[0]
            wf.write(t_id + ',' + '"'+t+'"'+','+y+','+p+','+ttime+'\n')
        
def main():
    with open('code.txt', 'r') as rf:
        gupiaos = get_codes(rf)

    for gp in gupiaos:
        tiezi_list[gp] = init_tiezi_set(gp)

    while True:
        for gp in gupiaos:
            update_tiezi_set(gp)
            print('Start to get %s: ....'%(gp))
            tiezi_urls = list(tiezi_list[gp])
            titles, yuedus, pingluns = get_yueping(tiezi_urls)
            with open('%s.csv'%gp, 'a', encoding='utf-8') as wf:
                writecsv(tiezi_urls, titles, yuedus, pingluns, wf)


if __name__ == '__main__':
    main()
    
