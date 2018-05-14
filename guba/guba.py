# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from postlist import PostList

GUBA_PING_URL = 'http://guba.eastmoney.com/list,%s_%d.html'
GUBA_FA_URL = 'http://guba.eastmoney.com/list,%s,f_%d.html'


class GuBa:
    def __init__(self, code, crawler, s_date, e_date, errfile, elock):
        self.code = code
        self.s_date = s_date
        self.e_date = e_date
        self.crawler = crawler
        self.errf = errfile
        self.elock = elock
        self.page = 100
        self.delta = 100
        self.is_search = 1
        self.searched_pages = []
        self.url = GUBA_FA_URL % (self.code, self.page)
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

    def check_tiezis(self, tiezis):
        if not tiezis:
            self.delta = 1
            return tiezis, True
        total_tiezis = len(tiezis)
        outdated_tiezis = 0
        cur_tiezis = 0
        new_tiezis = []
        for tiezi in tiezis:
            while not self.elock.acquire():
                self.elock.wait()
            try:
                t_year = int(tiezi['detail']['fa_date'].split('-')[0])
                if self.s_date <= t_year <= self.e_date:
                    new_tiezis.append(tiezi)
                    cur_tiezis = cur_tiezis + 1
                elif t_year < self.s_date:
                    outdated_tiezis = outdated_tiezis + 1
            except:
                total_tiezis = total_tiezis - 1
                self._write_err(
                    'Mist Error. Date of tiezi is not well structured: .',
                    tiezi['detail']['fa_date'], tiezi['url'], tiezi['pid'])
            finally:
                self.elock.release()
        if not self.is_search == 0:
            self.update_search(tiezis, cur_tiezis)
            return [], False
        if outdated_tiezis / total_tiezis > 0.5:
            print(outdated_tiezis, total_tiezis)
            return new_tiezis, True
        else:
            return new_tiezis, False

    def update_url(self):
        self.page = self.page + self.delta
        self.url = GUBA_FA_URL % (self.code, self.page)

    def update_search(self, tiezis, cur_tiezis):
        s = self._is_begin(tiezis)
        if s == 1 and cur_tiezis > 0:
            self.is_search = 0
            self.delta = 1
        elif s == 1 and self.delta == 100:
            self.is_search == 1
        elif s == 1 and cur_tiezis == 0:
            self.delta = max(abs(self.delta) // 2, 1)
            self.is_search = 1
        elif s == -1 and self.page not in self.searched_pages:
            self.delta = min(-abs(self.delta) // 2, -1)
            self.is_search = -1
        elif s == -1:
            self.is_search == 0
            self.delta = 1
        self.searched_pages.append(self.page)

    def _is_begin(self, tiezis):
        for tiezi in tiezis:
            try:
                s_year = int(tiezi['detail']['fa_date'].split('-')[0])
                break
            except:
                continue
        if s_year > self.s_date:
            return 1
        elif s_year <= self.s_date:
            return -1

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

    def _write_err(self, *kargs):
        self.errf.write('\n################\n')
        for arg in kargs:
            self.errf.write(arg)
            self.errf.write('\n')
        self.errf.write('################\n')
