# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


class TieZi:
    def __init__(self, resp, errfile=None):
        self.resp = resp
        self.errf = errfile
        if self.resp:
            self.set_tiezi(resp)

    def get_content(self):
        content = self.content.select('div#zwconbody div')[0].text.strip()
        return content

    def get_author(self):
        """Return:
                 author_id, author_name, author_url, fa_time, fa_device
        """
        author_sec = self.content.select('div#zwcontt div#zwconttb')[0]
        author = author_sec.select('div#zwconttbn strong a')[0]
        author_id = author['data-popper']
        author_name = author.text.strip()
        author_url = author['href']

        fa_info =  author_sec.select('div.zwfbtime')[0].text.strip()
        fa_time = ' '.join(fa_info.split(' ')[1:3])
        fa_device = fa_info.split(' ')[-1]

        return author_id, author_name, author_url, fa_time, fa_device

    def get_list(self):
        """Return: None: if no reply and end continue get replies
                   List of replies: [(id, author_name, author_id, author_url, content, is_reply, r_id, r_author_name, r_author_id, r_author_url, r_content),....]
"""
        if not self.reply_list:
            return None

        rl = []
        for r in self.reply_list:
            # get id
            r_id = r['data-huifuid']
            # get author
            r_author = r.select('div.zwlianame a')[0]
            r_author_name = r_author.text
            r_author_url = r_author['href']
            r_author_id = r_author['data-popper']
            # content
            content = r.select('div.zwlitext')[0].text.strip()
            # get reply content
            reply = r.select('div.zwlitalkbox div.zwlitalkboxtext')
            if not reply:
                is_reply = 0
                rr_id = ''
                rr_author_name = ''
                rr_author_id = ''
                rr_author_url = ''
                r_content = ''
            else:
                is_reply = 1
                rr_id = rr[0]['data-huifuid']
                rr_author_name = rr[0].select('a')[0].text
                rr_author_id = rr[0].select('a')[0]['data-popper']
                rr_author_url = rr[0].select('a')[0]['href']
                r_content = rr[0].select('a')[0].text.strip()
            rl.append((r_id, r_author_name, r_author_id, r_author_url, content, is_reply,
                       rr_id, rr_author_name, rr_author_id, rr_author_url, r_content))

        return rl

    def get_pager(self):
        return len(self.tiezi.select('div.pager')) > 0

    def set_tiezi(self, resp):
        self.resp = resp
        self.resp.encoding = 'utf-8'
        self.tiezi = BeautifulSoup(self.resp.text, 'html.parser')
        self.reply_list = self.tiezi.select('div#zwlist div.zwli')
