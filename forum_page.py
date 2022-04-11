import os.path

from lxml import etree
from tools import get_url
from tools import update_name
import time


def get_forum_page(url):

    # 打印网页源码
    html = etree.HTML(get_url(url).text)
    # result = etree.tostring(html, encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
    # print(result)
    list_url = []       # 分类导航总页数，每一页得地址列表
    list_detail_url = []
    forum_name = html.xpath("//h1[@class='xs2']//a/text()")[0]
    print("forum name: " + forum_name)

    if os.path.exists(forum_name + ".txt"):
        print("存在先删除")
        os.remove(forum_name + ".txt")
    if os.path.exists(forum_name + "_detail.txt"):
        print("存在先删除")
        os.remove(forum_name + "_detail.txt")

    page = html.xpath("//div[9]//span[1]//div[1]//label[1]//span[1]/text()")     # count page
    addr_title = url.split("/")[0] + "//" + url.split("/")[2] + "/"
    print("网页头为：" + addr_title)
    print("总页码为：" + page[0].split()[1])
    print(url.split("-"))
    print("列表网页头为：" + url.split("-")[0] + "-" + url.split("-")[1] + "-")
    print("最后一页地址为：" + url.split("-")[0] + "-" + url.split("-")[1] + "-" + page[0].split()[1] + ".html")

    for i in range(int(page[0].split()[1])):
        list_url.append(url.split("-")[0] + "-" + url.split("-")[1] + "-" + str(i + 1) + ".html")
        # print("当前地址为：" + url[0: -6] + str(i) + ".html")
        with open(forum_name + ".txt", "a") as f:
            f.write(url.split("-")[0] + "-" + url.split("-")[1] + "-" + str(i + 1) + ".html\r")
    for i in range(len(list_url)):
        # time.sleep(2)  # 暂停2秒继续
        print("正在获取" + list_url[i] + "页面数据")
        # tt = etree.HTML(get_url(list_url[i]).text).xpath('//*[@id="threadlisttableid"]/tbody/tr/th/a[2]')
        tt = etree.HTML(get_url(list_url[i]).text).xpath("(//th)")
        print("____" + str(len(tt)))

        lens = 0    # 需要循环th列表的长度
        ranges = 0  # 从第ranges位开始循环获取
        if list_url[i].endswith("-1.html"):      # 根据传入的分类页面链接，判断是否为第一页。
            print("从第一页还是导航")
            lens = len(tt) - 3
            ranges = 3
        else:
            print("从其他页面开始导航")
            lens = len(tt) - 2
            ranges = 2

        for j in range(lens):
            # print(etree.tostring(tt[j + ranges], encoding="utf-8", pretty_print=True, method="html").decode("utf-8"))
            bb = etree.HTML(
                etree.tostring(tt[j + ranges], encoding="utf-8", pretty_print=True, method="html").decode("utf-8"))
            thread_types = bb.xpath('//a/text()')[0]
            movie_detail_name = update_name(bb.xpath('//a/text()')[1])
            movie_detail_url = addr_title + bb.xpath('//a/@href')[2]
            print("thread types: " + thread_types)
            print("movie detail name: " + movie_detail_name)
            print("movie detail url: " + movie_detail_url)
            with open(forum_name + "_detail.txt", "a") as f:
                f.write(movie_detail_url + "\r")
            list_detail_url.append(movie_detail_url)
        print(len(list_detail_url))
    return list_detail_url, forum_name
