# -*- coding: utf-8 -*-

from tiezi import Tiezi

TIEZI_URL = 'http://guba.eastmoney.com/'


class PostList:
    def __init__(self, pl=None, errfile=None):
        self.pl = self.pl
        self.errf = errfile
        self.post = Tiezi(self.errf)

    def get_posts(self):
        '''Return: [(id, url, title, yuedu, pinglun), ...]   '''
        posts = []
        for x in self.posts_dom:
            if x.select('em'):
                continue
            url_doms = x.select('span.l3 a')
            if not url_doms:
                continue
            url = url_doms[0]['href']
            if 'http' in url:
                continue
            if '/' in url:
                url = url[1:]
            title = url_doms[0].text.strip()
            yuedu = x.select('span.l1')[0].text
            pinglun = x.select('span.l2')[0].text
            pid = url.split(',')[2].split('.')[0]
            posts.append((pid, TIEZI_URL+url, title, yuedu, pinglun))

        return posts

    def set_posts_list(self, pl):
        self.pl = pl
        self.posts_dom = self.pl.select('div#articlelistnew div.articleh')
