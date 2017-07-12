import os
from concurrent.futures import ThreadPoolExecutor
from urllib import request

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class CrawlThreadPool(object):
    def __init__(self):
        self.thread_pool=ThreadPoolExecutor(max_workers=os.cpu_count())

    def request_parse_runnable(self,url):
        print('start get web content from: %s' % url)
        try:
            headers={"User-Agent",
                           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
            req=request.Request(url,headers=headers)
            content=request.urlopen(req).read().decode('utf-8','igonre')
            soup=BeautifulSoup(content,"html.parser",from_encoding='utf-8')
            new_urls=set()
            links = soup.find_all('a', href=re.compile(r"/item/"))
            for link in links:
                new_url = link['href']
                new_full_url =urljoin(url, new_url)
                new_urls.add(new_full_url)
            data={"url":url,"new_urls":new_urls}
            data['title'] = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1').get_text()
            data['summary'] = soup.find('div', class_="lemma-summary").get_text()
        except BaseException as e:
            print("parse fail:%s"% e)
        return data

    def crawl(self,url,complete_callback):
        future=self.thread_pool.submit(self.request_parse_runnable(),url)
        future.add_done_callback(complete_callback)

class OutPutThreadPool(object):
    def __init__(self):
        self.thread_pool=ThreadPoolExecutor(max_workers=5)

    def output_runnable(self,crawl_result):
        url=crawl_result['url']
        title=crawl_result['title']
        summary=crawl_result['summary']
        print("result:%s ; %s ; %s" % (title,summary,url))

    def save(self,craw_result):
        self.thread_pool.submit(self.output_runnable(),craw_result)
class CrawlManager(object):
    def __init__(self):
        self.crawl_pool=CrawlThreadPool()
        self.output_pool=OutPutThreadPool()

    def start_runner(self,url):
        self.crawl_pool.crawl(url,self.crawl_future_callback())


    def crawl_future_callback(self,crawl_url_future):
        try:
            data=crawl_url_future.result()
            for new_url in data['new_urls']:
                self.start_runner(new_url)
            self.output_pool.save(data)
        except Exception as e:
            print('Run crawl url future thread error. %s'% e)

if __name__=='__main__':
     url="http://baike.baidu.com/item/Python"
    # manager=CrawlManager()
    # manager.start_runner(url)
