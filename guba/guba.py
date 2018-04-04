# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from postlist import PostList

GUBA_URL = 'http://guba.eastmoney.com/list,%s_%d.html'


class GuBa:
    def __init__(self, code, crawler, s_date, e_date, errfile):
        self.code = code
        self.s_date = s_date
        self.e_date = e_date
        self.crawler = crawler
        self.errf = errfile
        self.page = 1
        self.url = GUBA_URL % (self.code, self.page)
        self.postlist = PostList(self.crawler, self.errf)
        self.tiezis = []

    def fetch_posts_page(self):
        self.resp = self.crawler.fetch(self.url)
        if self.resp:
            self.resp.encoding = 'utf-8'
            self.pl = BeautifulSoup(self.resp.text, 'html.parser')
            self.postlist.set_posts_list(self.pl)
            return 1
        else:
            return 0

    def fetch_posts(self):
        new_tiezis = self.postlist.fetch_posts()
        new_tiezis, is_stop = self.check_tiezis(new_tiezis)
        self.tiezis.append(new_tiezis)
        return is_stop

    def get_pl(self):
        return self.pl

    def get_url(self):
        return self.url

    def check_tiezis(self, tiezis):
        for tiezi in tiezis:
        pass

    def update_url(self):
        self.page = self.page + 1
        self.url = GUBA_URL % (self.code, self.page)

    def run(self):
        is_stop = 0
        while not is_stop:
            flag = self.fetch_posts_page()
            if not flag:
                continue
            is_stop = self.fetch_posts()
        return self.tiezis
