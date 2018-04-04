# -*- coding: utf-8 -*-

import json
from guba import GuBa
from crawler import Crawler


columns = ['id', 'author_name', 'author_id', 'author_url', 'content', 'is_reply', 'r_id', 'r_author_name', 'r_author_id', 'r_author_url', 'r_content']


def main():
    with open('code.txt', 'r') as rf:
        codes = list(map(lambda x: x.strip(), rf.readlines()))

    crawler = Crawler('err.txt')
    results = {'std_err': 'err.txt', 'num': len(codes)}
    results['gubas'] = []
    for stock in codes:
        guba = GuBa(stock, crawler, '2016', '2017')
        tiezis = guba.run()
        guba_data = {'code': stock, 'num': len(tiezis)}
        guba_data['tiezis'] = tiezis
        results['gubas'].append(guba_data)
    with open('guba_data.json', 'w') as wf:
        json.dump(results, wf)


if __name__ == '__main__':
    main()
    

