# coding=gbk
'''
Created on 2016��1��17��

@author: zhong
'''
import urllib.request
import ssl


class HtmlDownLoader(object):
    def download(self, url):
        if url is None:
            return
        req = urllib.request.Request(url)
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
        data = urllib.request.urlopen(req,context=ssl._create_unverified_context()).read()

        return data.decode('UTF-8', 'igonre')
