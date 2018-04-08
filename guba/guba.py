# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from postlist import PostList

GUBA_URL = 'http://guba.eastmoney.com/list,%s_%d.html'


class GuBa:
    def __init__(self, code, crawler, s_date, e_date, errfile):
        self.code = code
        self.s_date = int(s_date)
        self.e_date = int(e_date)
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
        self.tiezis = self.tiezis + new_tiezis
        return is_stop

    def get_pl(self):
        return self.pl

    def get_url(self):
        return self.url

    def check_tiezis(self, tiezis):
        if not tiezis:
            return tiezis, True
        total_tiezis = len(tiezis)
        outdated_tiezis = 0
        new_tiezis = []
        for idx, tiezi in enumerate(tiezis):
            t_year = int(tiezi['detail']['fa_date'].split('-')[0])
            if self.s_date <= t_year <= self.e_date:
                new_tiezis.append(tiezi)
            elif t_year < self.s_date:
                outdated_tiezis = outdated_tiezis + 1
        if outdated_tiezis / total_tiezis > 0.5:
            return new_tiezis, True
        else:
            return new_tiezis, False

    def update_url(self):
        self.page = self.page + 1
        self.url = GUBA_URL % (self.code, self.page)

    def run(self):
        is_stop = False
        while not is_stop:
            flag = self.fetch_posts_page()
            if not flag:
                self.update_url()
            else:
                is_stop = self.fetch_posts()
                self.update_url()
        return self.tiezis
