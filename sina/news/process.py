# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
from news.content import gcrawler, aiocrawler


class News:
    def __init__(self, urls):
        self.urls = urls

    def fetch_contents(self):
        self.resps = gcrawler(self.urls)

    def aio_fetch_contents(self):
        self.resps = aiocrawler(self.urls)

    def get_artibody(self, resp):
        if type(resp) is bytes:
            page = resp.decode('gb2312')
        else:
            resp.encoding = 'gb2312'
            page = resp.text
        dom_page = BeautifulSoup(page, 'html.parser')
        return dom_page.select('div#artibody')


class Finnews(News):
    def __init__(self, urls):
        super().__init__(urls)

    def start(self):
        super().aio_fetch_contents()
        return len(self.resps)

    def get_content(self, i):
        r = self.resps[i]
        u = self.urls[i]
        if not r:
            return u
        else:
            artibody = super().get_artibody(r)
            if not artibody:
                return u
            article = []
            for p in artibody[0].select('p'):
                article.append(p.get_text())
            return '\n'.join(article)

    def get_keyword_content(self, i, keyword):
        r = self.resps[i]
        u = self.urls[i]
        if not r:
            return u
        else:
            artibody = super().get_artibody(r)
            if not artibody:
                return u
            article = []
            for p in artibody[0].select('p'):
                t = p.get_text()
                if keyword in t:
                    article.append(t)
                else:
                    continue

            return '\n'.join(article)
