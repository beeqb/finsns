import time
import re
import xlwt
import xlrd
from functools import *
from crawler import grcrawler
from bs4 import BeautifulSoup

URL1 = 'http://guba.eastmoney.com/list,%s_1.html'
URL2 = 'http://guba.eastmoney.com/list,%s_2.html'
TIEZI_URL = 'http://guba.eastmoney.com/%s'

def get_codes(cf):
    return list(map(lambda x: x.rstrip(), cf.readlines()))


def get_tiezi_urls(code):
    urls = [URL1%(code), URL2%(code)]
    resps = gcrawler(urls)
    list_pages = [BeautifulSoup(x.text, 'html.parser') for x in resps]
    tiezi_doms = [x.select('div#articlelistnew div.articleh') for x in list_pages]
    tiezi_list = reduce(lambda x, y: x+y, tiezi_doms)
    tiezi_urls = [x.select('span.l3 a')[0]['href'] for x in tiezi_list]

    return tiezi_urls


def get_yueping(urls):
    resps = gcrawler(urls)
    tiezis = [BeautifulSoup(x.text, 'html.parser') for  x in resps]
    yuedus = []
    pingluns = []
    titles = []
    for t in tiezis:
        zhuanping_doms = t.select('div#zwlist script')
        zhuanping_content = reduce(lambda x,y: x.text+y.text, zhuanping_doms)
        yuedu = re.search('var num=(.*?);.*', zhuanping_content).group(1)
        pinglun_pattern =  re.compile('.*var pinglun_num=(.*?);.*', re.S)
        pinglun= re.search(pinlun_pattern, zhuanping_content).group(1)
        title = t.select('div#zwconttbt')[0].text
        yuedus.append(yuedu)
        pingluns.append(pinglun)
        titles.append(title)

    return (titles, yuedus, pingluns)


def writecsv(titles, yuedus, pingluns, wf):
        ttime=time.strftime("%Y-%m-%d %H:%M", time.localtime())
        
# book_1=xlwt.Workbook(encoding='utf-8',style_compression=0)
# sheet_1=book_1.add_sheet('dede',cell_overwrite_ok=True)
# book_2=xlwt.Workbook(encoding='utf-8',style_compression=0)
# sheet_2=book_2.add_sheet('dede',cell_overwrite_ok=True)


def main:
    with open('code.txt', 'r') as rf:
        gupiaos = get_codes(rf)

    for gp in gupiaos:
            tiezi_urls = get_tiezi_urls(gp)
            titles, yuedus, pingluns = get_yueping(tiezi_urls)

    with open('%s.csv'%gp, 'w') as wf:
        writecsv(titles, yuedus, pingluns, wf)


if __name__ == '__main__':
    main()
    
