# -*- coding: utf-8 -*-


import grequests


class Crawler:
    def __init__(self, size=1000):
        self.size = size

    def gcrawler(self, urls):
        rs = (grequests.get(u, timeout=10) for u in urls)
        return grequests.map(rs, size=self.size)
