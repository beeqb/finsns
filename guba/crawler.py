# -*- coding: utf-8 -*-


import grequests
import time


class Crawler:
    def __init__(self, size=1000, errfile = None):
        self.size = size
        self.errfile = errfile

    def fetch(self, urls):
        rs = (grequests.get(u, timeout=10) for u in urls)
        resps = grequests.map(rs, size=self.size)
        resps, bad_urls, rs = self.check(resps, urls, 1)
        if not rs:
            return resps
        time.sleep(300)
        n_resps = grequests.map(rs, self.size)
        n_resps = self.check(n_resps, bad_urls, 2) 
        return resps+n_resps

    def check(self, resps, urls, rt):
        bad_urls = []
        for idx, (url, resp) in enumerate(zip(urls, resps)):
            if not resp:
                bad_urls.append(url)
                del resps[idx]
                if rt == 2:
                    self.write_err(resp.url, 'Nonetype. Maybe cannot connect to server or rejected.')
            elif resp.status_code == 200:
                continue
            elif resp.status_code == 404:
                self.write_err(resp.url, '404')
                del resps[idx]
            else:
                bad_urls.append(resp.url)
                del resps[idx]
                if rt == 2:
                    self.write_err(resp.url, resp.status_code)
        if bad_urls:
            if rt ==1:
                return resps, bad_urls, (grequests.get(u, timeout=10) for u in bad_urls)
            else:
                return resps
        else:
            if rt == 1:
                return resps, None, None
            else:
                return resps

    def write_err(self, url, errcode):
        self.errfile.write(url+',' + errcode + '\n')
