# coding=gbk
'''
Created on 2016年1月17日

@author: zhong
'''
import urllib.request


class HtmlDownLoader(object):
    def download(self, url):
        if url is None:
            return
        req = urllib.request.Request(url)
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
        data = urllib.request.urlopen(req).read()
        # data = urllib.request.urlopen(url, timeout=5).read()

        return data.decode('UTF-8', 'igonre')
