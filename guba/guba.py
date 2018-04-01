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
        self.url = GUBA_URL%(self.code, self.page)
        self.postlist = PostList(self.errf)
        self.tiezis = []

    def get_posts_page(self):
        self.resp = crawler.fetch([self.url])
        self.resp.encoding = 'utf-8'
        self.pl = BeautifulSoup(self.resp.text, 'html.parser')
        self.postlist.set_posts_list(self.pl)

    def get_pl(self):
        return self.pl

    def get_url(self):
        return self.url

    def update_url(self):
        self.page = self.page + 1
        self.url = GUBA_URL%(self.code, self.page)

    def run(self):
        self.get_posts_page()
