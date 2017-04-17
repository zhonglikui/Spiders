# coding=gbk
'''
Created on 2016��1��17��

@author: zhong
'''
import pymysql.cursors


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):

        # �������ݿ�
        connect = pymysql.Connect(host='localhost', port=3306, user='zhong', passwd='123456', db='baike',
                                  charset='utf8mb4')
        try:
            for data in self.datas:
                title = data['title']
                url = data['url']
                # ��ȡָ��
                with connect.cursor() as cursor:
                    # ����sql���
                    sql = "insert into `baike_data` (`name`,`url`) values (%s,%s)"
                    # ִ��sql���
                    cursor.execute(sql, (title, url))
                    connect.commit()
        finally:
            connect.close()

        connect = pymysql.Connect(host='localhost', port=3306, user='zhong', passwd='123456', db='baike',
                                  charset='utf8mb4')
        # ��ȡ���ݿ�
        try:
            with connect.cursor() as cursor:
                sql = "select `name`,`url` from `baike_data` where `id` is not null"
                count = cursor.execute(sql)
                print("����%s������" % (count))
                # result=cursor.fetchmany(size=9)
                result = cursor.fetchall()
                print(result)
        finally:
            connect.close()

        # fout = open('outfil.html', 'w', io.DEFAULT_BUFFER_SIZE, encoding='utf-8')
        # fout.write("<html>")
        # fout.write("<body>")
        # fout.write("<table border=\"1\">")
        # fout.write("<tr><th>id</th><th>url</th><th>title</th></tr>")
        # count = 0
        # for data in self.datas:
        #     count = count + 1
        #     title = data['title']
        #     url = data['url']
        #     fout.write("<tr>")
        #     fout.write("<td>%d</td>" % count)
        #     fout.write("<td>%s</td>" % url)
        #     fout.write("<td>%s</td>" % title)
        #
        #     fout.write("</tr>")
        #
        # fout.write("</table>")
        # fout.write("</body>")
        # fout.write("</html>")
        # fout.close()
        print("���")
