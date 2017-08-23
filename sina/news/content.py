from bs4 import BeautifulSoup
import grequests


def gget_content(urls):
    resps = gcrawler(urls)
    contents = []
    for r, u in zip(resps, urls):
        if not r:
            contents.append(u)
        else:
            r.encoding = 'utf-8'
            page = r.text
            dom_page = BeautifulSoup(page, 'html.parser')
            content = dom_page.select('div#artibody')
            if not content:
                return u
            article = []
            for p in content[0].select('p'):
                article.append(p.get_text())
            return ''.join(article)


def gcrawler(self, urls, ef):
    rs = (grequests.get(u) for u in urls)
    return grequests.map(rs)
