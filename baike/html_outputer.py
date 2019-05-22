# coding=gbk
'''
Created on 2016年1月17日

@author: zhong
'''
import sqlite3


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        # sqlite中的数据类型https://blog.csdn.net/u012917700/article/details/60115588
        conn = sqlite3.connect("baike.db")
        try:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS baike (id  integer PRIMARY KEY autoincrement ,name text, url text)")
            for data in self.datas:
                title = data['title']
                url = data['url']
                cursor.execute("INSERT INTO baike (name,url) VALUES (?,?)", (title, url))
            conn.commit()
        finally:
            conn.close()

        # connect = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', charset='utf8mb4')
        # try:
        #     with connect.cursor() as cursor:
        #         db = "CREATE DATABASE IF NOT EXISTS baike"
        #         cursor.execute(db)
        #         use = "USE baike"
        #         cursor.execute(use)
        #         table = "CREATE TABLE IF NOT EXISTS baike_data(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(64)NOT NULL,url VARCHAR(255)NOT NULL)"
        #         cursor.execute(table)
        #         for data in self.datas:
        #             title = data['title']
        #             url = data['url']
        #             sql = "insert into `baike_data` (`name`,`url`) values (%s,%s)"
        #             cursor.execute(sql, (title, url))
        #         connect.commit()
        # finally:
        #     connect.close()
        #
        # connect = pymysql.connect(host='localhost', port=3306, user='root', password='root', charset='utf8mb4')
        # # 读取数据库
        # try:
        #     with connect.cursor() as cursor:
        #         use = "USE baike"
        #         cursor.execute(use)
        #         sql = "select `name`,`url` from `baike_data` where `id` is not null"
        #         count = cursor.execute(sql)
        #         print("共有%s条数据" % (count))
        #         # result=cursor.fetchmany(size=9)
        #         result = cursor.fetchall()
        #         print(result)
        # finally:
        #     connect.close()
