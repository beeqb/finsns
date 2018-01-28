 # -*- coding: utf-8 -*-

import time
import re
from functools import *
import grequests
from bs4 import BeautifulSoup


URL1 = 'http://guba.eastmoney.com/list,%s_1.html'
URL2 = 'http://guba.eastmoney.com/list,%s_2.html'
TIEZI_URL = 'http://guba.eastmoney.com/'

tiezi_list = {}
tiezi_ids = {}


def gcrawler(urls):
    rs = (grequests.get(u, timeout=10) for u in urls)
    return grequests.map(rs, size=1000)


def get_codes(cf):
    return list(map(lambda x: x.rstrip(), cf.readlines()))


def init_tiezi_set(code):
    urls = [URL1 % (code), URL2 % (code)]
    resps = gcrawler(urls)
    try:
        list_pages = list(map(lambda x: BeautifulSoup(x.text, 'html.parser'), resps))
    except:
        print(urls)
    tiezi_urls = extract_list_pages(list_pages)
    for tu in tiezi_urls:
        tiezi_ids[tu] = tu.split(',')[2].split('.')[0]

    return tiezi_urls


def update_tiezi_set(code):
    gp_tiezi_set = tiezi_list[code]
    urls = [URL1 % (code)]
    resps = gcrawler(urls)
    try:
        list_pages = list(map(lambda x: BeautifulSoup(x.text, 'html.parser'), resps))
    except:
        print(urls)
    new_tiezi_urls = extract_list_pages(list_pages)
    for tu in new_tiezi_urls:
        tiezi_ids[tu] = tu.split(',')[2].split('.')[0]
    gp_tiezi_set.update(new_tiezi_urls)
    tiezi_list[code] = gp_tiezi_set


def extract_list_pages(list_pages):
    tiezi_doms = list(map(lambda x: x.select('div#articlelistnew div.articleh'), list_pages))
    tiezi_list = reduce(lambda x, y: x+y, tiezi_doms)
    tiezi_urls = []
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
    for idx, x in enumerate(resps):
        try:
            x.encoding = 'utf-8'
            tiezis.append(BeautifulSoup(x.text, 'html.parser'))
        except Exception as e:
            print('Error: ' + urls[idx], 'URL error. ', e)
            continue
    yuedus = []
    pingluns = []
    titles = []
    t_ids = []
    for u in urls:
        t_ids.append(tiezi_ids[u])
    for idx, t in enumerate(tiezis):
        zhuanping_doms = t.select('div#zwlist script')
        try:
            zhuanping_content = reduce(lambda x,y: x.text+y.text, zhuanping_doms)
        except Exception as e:
            print('Error: ', urls[idx], 'None Zhuan Ping content. ', e)
            continue
        yuedu = re.search('var num=(.*?);.*', zhuanping_content).group(1)
        pinglun_pattern = re.compile('.*var pinglun_num=(.*?);.*', re.S)
        pinglun = re.search(pinglun_pattern, zhuanping_content).group(1)
        title = t.select('div#zwconttbt')[0].text
        yuedus.append(yuedu)
        pingluns.append(pinglun)
        titles.append(title.strip())

    return (t_ids, titles, yuedus, pingluns)


def writecsv(t_ids, titles, yuedus, pingluns, wf):
        ttime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        for t_id, t, y, p in zip(t_ids, titles, yuedus, pingluns):
            wf.write(t_id + ','+'"'+t+'"'+','+y+','+p+','+ttime+'\n')


def main():
    with open('code.txt', 'r') as rf:
        gupiaos = get_codes(rf)

    for gp in gupiaos:
        tiezi_list[gp] = init_tiezi_set(gp)
        with open('%s.csv' % gp, 'w', encoding='utf-8') as wf:
            wf.write('id,title,yuedu,pinglun,time\n')

    while True:
        print('start')
        s_time = time.time()
        try:
            for gp in gupiaos:
                update_tiezi_set(gp)
                print('Start to get %s: ....' % (gp))
                tiezi_urls = list(tiezi_list[gp])
                t_ids, titles, yuedus, pingluns = get_yueping(tiezi_urls)
                with open('%s.csv' % gp, 'a', encoding='utf-8') as wf:
                    writecsv(t_ids, titles, yuedus, pingluns, wf)
            print('end')

            wait_time = 300 - (time.time() - s_time)
            if wait_time > 0:
                time.sleep(wait_time)
            else:
                print('Longer than 5mins: ', len(tiezi_ids))
                continue
        except KeyboardInterrupt:
            return 0
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    main()
