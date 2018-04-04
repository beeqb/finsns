# -*- coding: utf-8 -*-

from tiezi import TieZi

TIEZI_URL = 'http://guba.eastmoney.com/'


class PostList:
    def __init__(self, crawler=None, errfile=None):
        self.crawler = crawler
        self.errf = errfile
        self.pl = None
        self.post_detail = TieZi(self.crawler, self.errf)

    def fetch_posts(self):
        '''Return: [(id, url, title, yuedu, pinglun), ...]   '''
        posts = []
        for x in self.posts_dom:
            tiezi = {}
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
            tiezi['title'] = url_doms[0].text.strip()
            tiezi['yuedu'] = x.select('span.l1')[0].text
            tiezi['pinglun'] = x.select('span.l2')[0].text
            tiezi['pid'] = url.split(',')[2].split('.')[0]
            tiezi['url'] = TIEZI_URL + url
            tiezi['detail'] = self.get_post_details(tiezi['url'])
            posts.append(tiezi)
        return posts

    def get_post_details(self, url):
        self.post_detail.init_tiezi(url)
        return self.post_detail.fetch_tiezi_details()

    def set_posts_list(self, pl):
        self.pl = pl
        self.posts_dom = self.pl.select('div#articlelistnew div.articleh')
