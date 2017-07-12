from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from baike import url_manager, html_parser, html_downloader, html_outputer


class SpiderMain(object):
    def __init__(self):
        self.thread_pool=ThreadPoolExecutor()
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownLoader()
        self.praser = html_parser.HtmlPraser()
        self.outputer = html_outputer.HtmlOutputer()

    def crawl2(self,url):
        self.urls.add_new_urls(url)
        new_url=self.urls.get_new_url()
        htmlCount=self.downloader.download(new_url)
        new_urls,new_data=self.praser.prase(new_url,htmlCount)
        self.urls.add_new_urls(new_urls)
        return new_data;
    def craw(self, root_url):

        #------华丽的分割线------#
        # 添加新的url
        self.urls.add_new_url(root_url)
        # 当前的条数
        count = 1

        time1 = datetime.now()
        # 遍历所有的url

        while self.urls.has_new_url():
            try:
                # 获取一条url
                new_url = self.urls.get_new_url()

                print("%d : %s" % (count, new_url))

                # 下载网页
                html_cont = self.downloader.download(new_url)

                # 解析网页，得到新的url列表和数据
                new_urls, new_data = self.praser.prase(new_url, html_cont)
                # 将url列表添加的url管理器
                self.urls.add_new_urls(new_urls)
                # 收集数据
                self.outputer.collect_data(new_data)

                if count == 99:
                    break

                count = count + 1
            except(Exception) as e:
                print("craw fail:%s" % (e))

        # 输出收集好的数据
        self.outputer.output_html()
        time2 = datetime.now()
        print("耗时 %s 秒" % (time2 - time1).seconds)#23-21

    def start(self,url):
        future=self.thread_pool.submit(self.crawl2,url)
        future.add_done_callback(self.crawl_future_callback)

    def crawl_future_callback(self, crawl_url_future):
        time1=datetime.now()
        try:
            count=0;
            data = crawl_url_future.result()
            print(data['title'], data['url'])
            new_url = self.urls.get_new_url()
            self.start_runner(new_url)
            self.outputer.collect_data(data)

        except Exception as e:
            print('Run crawl url future thread error. '+str(e))
        self.outputer.output_html()
        time2 = datetime.now()
        print("耗时 %s 秒" % (time2 - time1).seconds)# 23 - 21

if __name__ == "__main__":
    root_url = "http://baike.baidu.com/item/Python"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
    #obj_spider.start(root_url)

