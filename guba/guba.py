# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


class GuBa:
    def __init__(self, resp):
        self.resp = resp
        self.resp.encoding = 'utf-8'
        self.pl = BeautifulSoup(self.resp.text, 'html.parser')

    def get_posts_pages(self):


    def set_guba(self, resp):
        self.resp = resp
        self.resp.encoding = 'utf-8'
        self.pl = BeautifulSoup(self.resp.text, 'html.parser')

    def get_pl(self):
        return self.pl
