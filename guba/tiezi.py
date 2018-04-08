# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

class TieZi:
    def __init__(self, crawler=None, errfile=None):
        self.crawler = crawler
        self.resp = None
        self.url = ''
        self.errf = errfile
        self.tiezi = {}
        self.base_url = ''
        self.content = None
        self.page = 1

    def get_content(self):
        content = self.content.select('div#zwconbody div')[0].prettify()
        return content

    def get_author(self):
        """Return:
                 author_id, author_name, author_url, fa_date, fa_time, fa_device
        """
        try:
            author_sec = self.content.select('div#zwcontt div#zwconttb')[0]
        except IndexError:
            self._write_err(self.resp.url, 'Get post author section failed')
            return ('' for i in range(6))
        author = author_sec.select('div#zwconttbn strong a')[0]
        author_id = author['data-popper']
        author_name = author.text.strip()
        author_url = author['href']
        fa_info = author_sec.select('div.zwfbtime')[0].text.strip()
        fa_date = fa_info.split(' ')[1]
        fa_time = fa_info.split(' ')[2]
        fa_device = fa_info.split(' ')[-1]
        return author_id, author_name, author_url, fa_date, fa_time, fa_device

    def get_reply_list(self):
        """Return: None: if no reply and end continue get replies
                   List of replies: [(id, author_name, author_id, author_url, content, date, time, is_reply, r_id, r_author_name, r_author_id, r_author_url, r_content),....]
"""
        if not self.reply_list:
            return None
        rl = []
        for i, r in enumerate(self.reply_list):
            # get id
            r_el = {}
            r_el['r_id'] = r['data-huifuid']
            # get author
            r_author = r.select('div.zwlianame a')
            if r_author:
                r_author = r_author[0]
                r_el['r_author_name'] = r_author.text.strip()
                r_el['r_author_url'] = r_author['href']
                r_el['r_author_id'] = r_author['data-popper']
            else:
                try:
                    r_el['r_author_name'] = r.select('div.zwlianame span.gray')[0].text
                except IndexError:
                    self._write_err(self.resp.url, str(i) + ' reply', 'Get reply list error', r.prettify())
                    continue
            try:
                r_el['content'] = r.select('div.zwlitext')[0].prettify()
                r_el['r_date'] = r.select('div.zwlitime')[0].text.split(' ')[1]
                r_el['r_time'] = r.select('div.zwlitime')[0].text.split(' ')[2]
            except IndexError:
                self._write_err(self.resp.url, str(i) + ' reply', 'Get reply content/datetime error', r.prettify())
                continue
            try:
                reply = r.select('div.zwlitalkbox div.zwlitalkboxtext')
                if not reply:
                    r_el['is_reply'] = 0
                    # r_el['rr_id'] = ''
                    # r_el['rr_author_name'] = ''
                    # r_el['rr_author_id'] = ''
                    # r_el['rr_author_url'] = ''
                    # r_el['r_content'] = ''
                else:
                    r_el['is_reply'] = 1
                    r_el['rr_id'] = reply[0]['data-huifuid']
                    r_el['rr_author_name'] = reply[0].select('a')[0].text
                    r_el['rr_author_id'] = reply[0].select('a')[0]['data-popper']
                    r_el['rr_author_url'] = reply[0].select('a')[0]['href']
                    r_el['r_content'] = reply[0].select('a')[0]
            except IndexError:
                self._write_err(self.resp.url, str(i) + ' reply', 'Get Re-reply list error', reply[0].prettify())
                continue
            rl.append(r_el)
        return rl

    def get_next_page(self):
        self.page = self.page + 1
        url_base = self.base_url.split('.html')[0]
        url = url_base + '_%d' % self.page + '.html'
        return self._fetch_tiezi(url)

    def init_tiezi(self, url):
        self.base_url = url
        return self._fetch_tiezi(url)

    def _fetch_tiezi(self, url):
        self.resp = self.crawler.fetch(url)
        if self.resp:
            self.resp.encoding = 'utf-8'
            self.content = BeautifulSoup(self.resp.text, 'html.parser')
            self.reply_list = self.content.select('div#zwlist div.zwli')
            return 1
        else:
            return 0

    def fetch_tiezi_details(self):
        if not self.resp:
            return 0
        try:
            self.tiezi['content'] = self.get_content()
        except IndexError as e:
            self._write_err(self.resp.url, 'Get content error.')
        self.tiezi['author_id'],\
        self.tiezi['author_name'],\
        self.tiezi['author_url'],\
        self.tiezi['fa_date'],\
        self.tiezi['fa_time'],\
        self.tiezi['fa_device'] = self.get_author()
        self.tiezi['replies'] = []
        while True:
            replies = self.get_reply_list()
            if not replies:
                break
            self.tiezi['replies'] = self.tiezi['replies'] + replies
            if not self.get_next_page():
                break
        return self.tiezi

    def _write_err(self, url, *kargs):
        self.errf.write('\n###################\n'+url+'\n')
        for arg in kargs:
            self.errf.write(arg)
            self.errf.write('\n')
        self.errf.write('######################\n')