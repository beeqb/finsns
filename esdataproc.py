import json
import unicodecsv as csv

N_FILES = 3
PREFIX = 't'
FIELDNAMES = ["id","crawler_time","is_retweet","user_id","nick_name","tou_xiang","user_type","weibo_id","weibo_content","zhuan","ping","zan","url","device","locate","time","pic_content"]

def readfile(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def initcsv(csvfile):
    writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
    writer.writeheader()
    return writer

def writecsv(writer, data):
    for i in range(len(data)):
        writer.writerow(data[i]['_source'])


def main():
    with open('data.csv', 'wb') as csvfile:
        writer = initcsv(csvfile)
        for i in range(N_FILES):
            data = readfile(PREFIX+str(i)+'.txt')
            writecsv(writer, data['hits']['hits'])


if __name__ == '__main__':
    print 'Start...'
    main()
