# -*- coding: utf-8 -*-

import pickle
import time
from gevent.pool import Pool
from gevent.lock import BoundedSemaphore
from guba import GuBa
from crawler import Crawler
import sys;sys.setrecursionlimit(100000)


def get_stock(stock, crawler, errfile, elock):
    print('Start to fetch %s:...' % stock)
    s_t = time.time()
    guba = GuBa(stock, crawler, 2016, 2017, errfile, elock)
    tiezis = guba.run()
    guba_data = {'code': stock, 'tiezis': tiezis}
    e_t = time.time()
    print(e_t - s_t, 's finish.')
    with open('%s.pkl' % stock, 'wb') as wf:
        pickle.dump(guba_data, wf)
    print('Finish fetching %s.' % stock)
    return 1


def main():
    with open('code_test.txt', 'r') as rf:
        codes = list(map(lambda x: x.strip(), rf.readlines()))
    cerrfile = open('err.txt', 'w')
    perrfile = open('html_parse_err.txt', 'w')

    crawler = Crawler(errfile=cerrfile)
    pool = Pool(1000)
    elock = BoundedSemaphore()

    #pars = pool.map(lambda c: get_stock(c, crawler, perrfile, elock), codes)
    for stock in codes:
        get_stock(stock, crawler, perrfile, elock)
    #pool.join()


if __name__ == '__main__':
    main()
    

