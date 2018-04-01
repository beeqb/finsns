# -*- coding: utf-8 -*-

import pandas as pd
from guba import GuBa
from crawler import Crawler


columns = ['id', 'author_name', 'author_id', 'author_url', 'content', 'is_reply', 'r_id', 'r_author_name', 'r_author_id', 'r_author_url', 'r_content']


def main():
    with open('code.txt', 'r') as rf:
        codes = list(map(lambda x:x.strip(), rf.readlines()))

    crawler = Crawler('err.txt')
    for stock in codes:
        guba = GuBa(stock, crawler, '2016-1-1', '2017-12-31')
        tiezis = guba.run()
        guba_data = pd.DataFrame(tiezis, columns=columns)
        guba_data.to_csv('%s.csv'%stock, sep='\t', encoding='utf-8')


if __name__ == '__main__':
    main()
    

