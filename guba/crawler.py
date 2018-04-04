# -*- coding: utf-8 -*-


import gevent
from gevent import monkey;monkey.patch_all()
import requests
from requests.exceptions import *
import grequests


class Crawler:
    def __init__(self, size=1000, errfile = None):
        self.size = size
        self.errfile = errfile

    def mfetch(self, urls):
        rs = (grequests.get(u, timeout=10) for u in urls)
        resps = grequests.map(rs, size=self.size)
        resps, bad_urls, rs = self._check(resps, urls, 1)
        if not rs:
            return resps
        gevent.sleep(300)
        n_resps = grequests.map(rs, self.size)
        n_resps = self._check(n_resps, bad_urls, 2)
        return resps+n_resps

    def fetch(self, url):
        resp = None
        is_finish = False
        while True:
            try:
                resp = requests.get(url, timeout=10)
                if not resp.status_code == 200:
                    resp = None
                    self._write_err(url, resp.status_code)
                is_finish = True
            except Timeout:
                if is_finish:
                    self._write_err(url, 'Connection Failed. Maybe blocked by server.')
                    break
                gevent.sleep(300)
            except RequestException as e:
                self._write_err(url, e)
                is_finish = True
            finally:
                if is_finish:
                    return resp
                else:
                    is_finish = True

    def _check(self, resps, urls, rt):
        bad_urls = []
        for idx, (url, resp) in enumerate(zip(urls, resps)):
            if not resp:
                bad_urls.append(url)
                del resps[idx]
                if rt == 2:
                    self._write_err(resp.url, 'Nonetype. Maybe cannot connect to server or rejected.')
            elif resp.status_code == 200:
                continue
            elif resp.status_code == 404:
                self._write_err(resp.url, '404')
                del resps[idx]
            else:
                bad_urls.append(resp.url)
                del resps[idx]
                if rt == 2:
                    self._write_err(resp.url, resp.status_code)
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

    def _write_err(self, url, errcode):
        self.errfile.write(url+',' + errcode + '\n')