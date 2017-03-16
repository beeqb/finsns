import requests
import codecs
from cookies import getCookies
from settings import getUsers


def main():
    myWeiBo = getUsers('settings.txt')
    cookies = getCookies(myWeiBo)
    print "Get Cookies Finish!( Num:%d)" % len(cookies)

    base_url = 'http://weibo.cn/'
    ids = '2420767405'
    r = requests.get(base_url+ids+'/profile?filter=1&page=1', cookies=cookies[0])
    with codecs.open('spdbank.txt', 'w', encoding='utf-8') as f:
        f.write(r.text)


if __name__ == '__main__':
    print 'Start...'
    main()
    print 'Ok'
