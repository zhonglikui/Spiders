# coding=utf-
#https://blog.csdn.net/Luenci379/article/details/90728048
from bs4 import BeautifulSoup
import os

all_url = 'http://www.mzitu.com'

# http请求头
Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://www.mzitu.com'
}
Picreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://i.meizitu.net'
}
# 此请求头破解盗链

start_html = requests.get(all_url, headers=Hostreferer)

# 保存地址
path = "D:\\mzitu\\"

# 找寻最大页数
soup = BeautifulSoup(start_html.text, "html.parser")
page = soup.find_all('a', class_='page-numbers')
max_page = page[-2].text

same_url = 'http://www.mzitu.com/all/'
for n in range(1, int(max_page) + 1):
    ul = same_url + str(n)
    start_html = requests.get(ul, headers=Hostreferer)
    soup = BeautifulSoup(start_html.text, "html.parser")
    all_a = soup.find('div', class_='all').find_all('a', target='_blank')
    for a in all_a:
        title = a.get_text()  # 提取文本
        if (title != ''):
            print("准备扒取：" + title)

            # win不能创建带？的目录
            if (os.path.exists(path + title.strip().replace('?', ''))):
                # print('目录已存在')
                flag = 1
            else:
                os.makedirs(path + title.strip().replace('?', '').replace(':', ''))
                flag = 0
            os.chdir(path + title.strip().replace('?', '').replace(':', ''))
            href = a['href']
            html = requests.get(href, headers=Hostreferer)
            mess = BeautifulSoup(html.text, "html.parser")
            pic_max = mess.find_all('span')
            try:
                pic_max = pic_max[9].text  # 最大页数
                if (flag == 1 and len(os.listdir(path + title.strip().replace('?', ''))) >= int(pic_max)):
                    print('已经保存完毕，跳过')
                    continue
                for num in range(1, int(pic_max) + 1):
                    pic = href + '/' + str(num)
                    html = requests.get(pic, headers=Hostreferer)
                    mess = BeautifulSoup(html.text, "html.parser")
                    pic_url = mess.find('img', alt=title)
                    print(pic_url['src'])
                    # exit(0)
                    html = requests.get(pic_url['src'], headers=Picreferer)
                    file_name = pic_url['src'].split(r'/')[-1]
                    f = open(file_name, 'wb')
                    f.write(html.content)
                    f.close()
            except Exception:
                pass
            print('完成   ')
    print('第', n, '页完成')
