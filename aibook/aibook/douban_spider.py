# 爬取豆瓣图书信息的爬虫
import requests
from bs4 import BeautifulSoup
import time
import csv
import pymysql
# 从Chrome浏览器复制User-Agent，将其伪装成浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                 ' like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}

url = "https://book.douban.com/tag/小说?start={}&type=T"



#  爬取一页的图书信息
def get_info(url):
    list = []  # 存储爬到的图书信息
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text.encode('utf-8'), 'lxml')
    #print(soup.text)
    # 使用beautifulsoup解析代码,注意第一个参数的.text
    books = soup.select('ul.subject-list>li')
    for book in books:
        #print(book)
        # name = book.select_one('div.info>h2>a').get_text().strip()  # 书名,有的有副标题，在get_tag里获得书名
        infos = book.select_one('div.pub').get_text().strip().split('/')  # 基本信息
        if len(infos) < 4:  # 如果图书信息少于四项则跳过
            continue
        price = infos[-1]  # 定价
        time = infos[-2]  # 出版年
        publisher = infos[-3]  # 出版社
        # 作者与译者
        if len(infos)==4:
            writer = infos[0]
        elif (len(infos[1])+len(infos[0]))<30:
            writer = infos[0]+','+infos[1]+'译'
        else:
            writer = infos[0]
        # 评分和读者数
        rate = book.select_one('div>span.rating_nums').get_text()
        rate_nums_data = book.select_one('div>span.pl').get_text().strip()
        rate_nums=rate_nums_data[1:rate_nums_data.find('人')]  # 只取评分人数
        href = book.find('a',attrs={'class': ''},href=True).attrs['href']  # 获得图书链接

        data = {
            'writer':writer,
            'price':price,
            'time':time,
            'publisher':publisher,
            'rate':rate,
            'rate_nums':rate_nums
        }
        data2=get_tag(href)
        data.update(data2)  # 将简介和标签信息加到data
        #print(data)
        if len(data['intro'])<2000:
            list.append(data)
    return list

def get_tag(href):  # 在图书页面获取分类标签，以及简介
    time.sleep(0.5)
    res = requests.get(href, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text.encode('utf-8'), 'lxml')
    #  爬书名
    name = soup.select_one('div>h1>span').get_text().strip()
    #print(name)
    #  爬图书简介
    all = soup.select('span.all>div>div.intro>p')
    if len(all)!=0:  # 如果被折叠
        ls3=[]
        for i in range(len(all)):
            ls3.append(all[i].get_text())
        intro = '<br>'.join(ls3)
    else:  # 没被折叠
        intros = soup.select('div.intro > p')
        ls =[]
        for i in range(len(intros)-1):  # 不爬作者简介
            ls.append(intros[i].get_text())
        intro = '<br>'.join(ls)  # 每一段后换行
    #print(intro)
    #  爬分类标签
    tags = soup.select('div.indent>span>a')
    ls2=[]
    for i in range(len(tags)):
        ls2.append(tags[i].get_text())
    tag = '/'.join(ls2)
    data ={
        'name':name,
        'intro':intro,
        'tags':tag
    }
    return data

# 存储到数据库aibook
def save_db(data):
    db = pymysql.connect(host="localhost", user="root", passwd="666", db="aibook2",charset='utf8mb4')
    #获取游标
    cursor = db.cursor()
    for book in data:
        print(book)
        sql="insert into books(bname,writer,price,time,publisher,rate,rate_nums,intro,tags) values" \
            "('{}','{}','{}','{}','{}',{},{},'{}','{}')"\
            .format(book['name'],book['writer'],book['price'],book['time'],book['publisher'],
                    book['rate'],book['rate_nums'],book['intro'],book['tags']
            )
        print(sql)
        cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    data1=get_info(url.format(0))
    save_db(data1)
    time.sleep(0.5)
    # 爬取2-10页的内容
    for i in range(20, 180,20):
        save_db(get_info(url.format(i)))
        time.sleep(0.5)
