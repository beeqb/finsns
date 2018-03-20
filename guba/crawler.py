# -*- coding: utf-8 -*-


import grequests

def gcrawler(self, urls):
    rs = (grequests.get(u, timeout=10) for u in urls)
    return grequests.map(rs, size=1000)
