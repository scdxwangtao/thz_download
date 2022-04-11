import logical_page
from detail_page import get_detail_page
from forum_page import get_forum_page
from grab import Grab
import time
from lxml import etree
import tools
import my_pools


def test_forum_page(forum_url):
    return get_forum_page(forum_url)


def test_detail_page():
    """
    test detail page
    :return:
    """
    # get_detail_page('http://91thz.cc/thread-329492-1-512.html')     # 多张图片的，双BT磁力的
    # get_detail_page('http://91thz.cc/thread-1996956-1-200.html')     # 多张图片的，双BT磁力的
    # get_detail_page('http://91thz.cc/thread-19118-1-593.html')      # 种子文件在上边
    # get_detail_page('http://91thz.cc/thread-31792-1-588.html')      # 详细信息在中间
    # get_detail_page('http://91thz.cc/thread-52119-1-584.html')      # 种子文件在中间
    # get_detail_page('http://91thz.cc/thread-2480549-1-1.html')      # 传入分类地址链接, 第三方种子链接
    # get_detail_page('http://91thz.cc/thread-2294804-1-1.html')      # 传入分类地址链接
    # get_detail_page('http://91thz.cc/thread-723253-1-1.html')       # 传入分类地址链接
    # get_detail_page('http://91thz.cc/thread-1996956-1-200.html')      # 传入分类地址链接
    get_detail_page('http://91thz.cc/thread-52119-1-584.html')      # 传入分类地址链接
    # get_detail_page('http://91thz.cc/thread-706873-1-1.html')       # 传入分类地址链接
    # get_detail_page('http://91thz.cc/thread-49235-1-584.html')       # 传入分类地址链接
    # get_detail_page('http://91thz.cc/thread-2487565-1-1.html')      # 传入分类地址链接
    # get_detail_page('http://91thz.cc/thread-2294471-1-1.html')      # 传入分类地址链接
    # get_detail_page('http://91thz.cc/thread-27653-1-590.html')      # 传入分类地址链接
    # get_detail_page("http://91thz.cc/thread-326870-1-512.html")     # 两个种子链接
    # get_detail_page("http://91thz.cc/thread-89479-1-572.html")      # 图片需要其他方式获取的
    # get_detail_page("http://91thz.cc/thread-2487565-1-1.html")      # 正常两张图片的
    # get_detail_page("http://91thz.cc/thread-2487565-1-1.html")      # 正常两张图片的


def test_grab():
    g = Grab()
    resp = g.go('www.baidu.com')
    print(type(resp))
    print(resp.charset)
    # print(resp.body)
    print(resp.unicode_body())


def test_readfile(forum_names):
    """

    :param forum_names:
    :return:
    """
    with open(forum_names + "_detail.txt", "r") as r:
        return r.readlines()


def test_save_image(url):
    addr_title = url.split("/")[0] + "//" + url.split("/")[2] + "/"  # Get home page address
    print("Home page address： " + addr_title)

    html = etree.HTML(tools.get_url(url).text)  # Add the retrieved page content to xpath.
    text = html.xpath("//div[contains(@class,'t_fsz')]/table")  # Gets part of the details page.
    name = html.xpath('//*[@id="thread_subject"]/text()')  # Gets the save name.
    name = tools.update_name(name[0])  # Example Modify the name of an invalid file.
    tools.mkdir("test/" + name)
    logical_page.parse_save_image(text, addr_title)

# def test_thread():
#     thread.start_new_thread(print_time, ("Thread-1", 2,))
#     thread.start_new_thread(print_time, ("Thread-2", 4,))


if __name__ == '__main__':
    # forum_name = "亚洲無碼原創"
    # forum_name = "欧美無碼"
    # forum_name = "国内原创(BT)"
    # forum_name = "蓝光高清原盘"
    # test_save_image("http://91thz.cc/thread-11561-1-594.html")
    # detail_urls, forum_name = test_forum_page("http://91thz.cc/forum-181-1.html")       # 亚洲无码
    # detail_urls, forum_name = test_forum_page("http://91thz.cc/forum-182-1.html")       # 欧美无码
    # detail_urls, forum_name = test_forum_page("http://91thz.cc/forum-69-1.html")       # 国内原创
    detail_urls, forum_name = test_forum_page("http://91thz.cc/forum-177-1.html")       # 蓝光高清原盘
    # print(len(detail_urls))
    # print(forum_name)

    # for i in range(detail_urls):
    #     test_detail_page(detail_urls[i])

    test_detail_page()
    # detail_urls = tools.read_file(forum_name)
    # for i in range(len(detail_urls)):
    #     print(detail_urls[i])

    # print(tools.count_lines("亚洲無碼原創.txt"))

    # my_pools.detail_pool(forum_name, get_detail_page, 128)
    # logical_page.delete_empty_files("data/亚洲無碼原創")
    # logical_page.delete_empty_files("data/欧美無碼")
    # logical_page.delete_empty_files("data/国内原创_BT_")
