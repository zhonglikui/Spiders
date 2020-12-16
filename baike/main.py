from datetime import datetime
import time

from baike import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownLoader()
        self.praser = html_parser.HtmlPraser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):

        # 添加新的url
        self.urls.add_new_url(root_url)
        # 当前的条数
        count = 1
        self.task(count)
        count = count + 1
        time.sleep(3)
        time1 = datetime.now()
        # 遍历所有的url
        # pool = Pool(cpu_count())
        #
        # while self.urls.has_new_url():
        #     pool.apply(func=self.task,args=(count,))
        #     if count == 99:
        #         break
        #     count = count + 1
        # pool.close()
        # pool.join()
        while self.urls.has_new_url():
            self.task(count)
            if count == 99:
                break
            count = count + 1

            # 输出收集好的数据
        self.outputer.output_html()
        time2 = datetime.now()
        print("耗时 %s 秒" % (time2 - time1).seconds)  # 23-21

    def task(self, count):
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
        except(Exception) as e:
            print("craw fail:%s" % (e))


if __name__ == "__main__":
    root_url = "https://baike.baidu.com/item/Python/407313"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
