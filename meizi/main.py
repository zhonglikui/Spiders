import datetime
import multiprocessing
import time
import urllib.request
from multiprocessing import Pool

import chardet
from bs4 import BeautifulSoup


def downloadImage(imageUrl):
    print("开始下载%s" % imageUrl)
    req = urllib.request.Request(imageUrl)
    req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)")
    req.add_header("Referer", "http://i.meizitu.net")
    f = open("%s.jpg" % str(time.time()), "wb")
    f.write(urllib.request.urlopen(req).read())
    f.close()


def getHtml(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    req.add_header("Accept-Encoding", "gzip, deflate, sdch")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.8")
    data = urllib.request.urlopen(req).read()
    print(chardet.detect(data))
    return data.decode('GB2312', 'igonre')


if __name__ == "__main__":

    url = "http://www.meizitu.com/a/pure_1.html"
    result = getHtml(url)

    soup = BeautifulSoup(result, 'html.parser')
    all_a = soup.find('ul', class_='wp-list clearfix').find_all(
        "img")  # .find_all('a', target='_blank')#,href=re.compile('limg.jpg')
    pool = Pool(multiprocessing.cpu_count())
    t1 = datetime.datetime.now()
    for a in all_a:
        src = a['src']
        pool.apply_async(downloadImage, args=(src,))
    pool.close()
    pool.join()

    t2 = datetime.datetime.now()
    print("耗时 %s 秒" % (t2 - t1).seconds)  # 23-21
