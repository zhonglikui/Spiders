# coding=gbk
'''
Created on 2016��1��17��

@author: zhong
'''
import pymysql


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):

        # �������ݿ�
        connect = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', charset='utf8mb4')
        try:
            with connect.cursor() as cursor:
                db = "CREATE DATABASE IF NOT EXISTS baike"
                cursor.execute(db)
                use = "USE baike"
                cursor.execute(use)
                table = "CREATE TABLE IF NOT EXISTS baike_data(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(64)NOT NULL,url VARCHAR(255)NOT NULL)"
                cursor.execute(table)
                for data in self.datas:
                    title = data['title']
                    url = data['url']
                    sql = "insert into `baike_data` (`name`,`url`) values (%s,%s)"
                    cursor.execute(sql, (title, url))
                connect.commit()
        finally:
            connect.close()

        connect = pymysql.connect(host='localhost', port=3306, user='root', password='root', charset='utf8mb4')
        # ��ȡ���ݿ�
        try:
            with connect.cursor() as cursor:
                use = "USE baike"
                cursor.execute(use)
                sql = "select `name`,`url` from `baike_data` where `id` is not null"
                count = cursor.execute(sql)
                print("����%s������" % (count))
                # result=cursor.fetchmany(size=9)
                result = cursor.fetchall()
                print(result)
        finally:
            connect.close()
