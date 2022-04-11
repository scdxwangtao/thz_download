import os

from lxml import etree

import tools
from tools import get_url, save_image


def save_movie_information(path, text, name, detail_url):
    ss = etree.HTML(etree.tostring(text[0], encoding="utf-8", pretty_print=True, method="html").decode("utf-8"))
    message = ss.xpath("//text()")  # gets text list
    print(name + "/" + name + "_movie_information.txt")
    print("Start saving movie information to directory: data/" + name)
    with open(path + name + "_movie_information.txt", 'w',
              encoding='utf-8') as f:  # Directory to save files.
        for i in message:
            if i not in ['\r\n\r\n', '\r\n', '\r', '\n', ' ']:
                f.write(i.strip("\r\n"))
                f.write("\r\n")
        f.write("【Detail url】：" + detail_url + "\n")
        f.write("【Email address】：thz@gmail.com")
    print("Succeeded in saving movie information to directory.")


def parse_save_image(path, html, addr_title):
    """
    Method of saving images
    :param path: save path
    :param addr_title: Web title
    :param html: Xpath-processed HTML
    :return:
    """
    text = html.xpath("//div[contains(@class,'t_fsz')]/table")  # Gets part of the details pageee.
    # Gets part of the details pageee.
    name = html.xpath('//*[@id="thread_subject"]/text()')[0]  # Get the original name.
    if len(html.xpath("//ignore_js_op/dl/dd/div/div/p/a[@target='_blank']/@href")) != 0:
        print("=======第一种方法======")
        img_s = html.xpath("//ignore_js_op/img/@zoomfile") + html.xpath(
            "//ignore_js_op/dl/dd/div/div/p/a[@target='_blank']/@href")
    elif len(html.xpath("(//img[@title='{}'])/@src".format(name))) != 0:
        print("=======第二种方法======")
        img_s = html.xpath("(//img[@title='{}'])/@src".format(name))
    elif len(etree.HTML(etree.tostring(text[0][0], encoding="utf-8", pretty_print=True, method="html").
                                decode("utf-8")).xpath("//@file")) != 0:
        print("=======第三种方法======")
        img_s = etree.HTML(etree.tostring(text[0][0], encoding="utf-8", pretty_print=True, method="html").
                           decode("utf-8")).xpath("//@file")  # gets images list

    else:
        if html.xpath("(//div[@class='pattl'])[2]") is not None:
            print("=======第四种方法======")
            img_s = etree.HTML(etree.tostring(html.xpath("(//div[@class='pattl'])[2]")[0], encoding="utf-8",
                                              pretty_print=True, method="html").decode("utf-8")).xpath("//@file")
        else:
            img_s = []

    name = tools.update_name(name)
    for j in range(len(img_s)):
        if img_s[j].startswith("http:"):  # http开头
            img_s_url = img_s[j]
        else:
            img_s_url = addr_title + img_s[j]
        print("The address of the {} picture is: ".format(j) + img_s_url)
        save_image(path, img_s_url, name, j)


def parse_seed_file_address(html, addr_title):
    """
    A method to parse the address of a seed file
    :param html:    Add the retrieved page content to xpath.
    :param addr_title:  Address title
    :return:    seed_page_address, seed_file_address, referer
    """

    seed_page_address = []  # The seed page address obtained from the detail page.
    seed_file_address = []  # Seed file address

    if len(html.xpath("//p[@class='attnm']//a/@href")) != 0:  # 判断磁力链接保存方式,第一种方式
        for i in range(len(html.xpath("//p[@class='attnm']//a/@href"))):
            seed_page_address.append(addr_title + (html.xpath("//p[@class='attnm']//a/@href")[i]))
            if get_url(seed_page_address[i]).text is not None:
                seed_file_address.append(etree.HTML(get_url(seed_page_address[i]).text).
                                         xpath("//body/div[@class='wp']/div[@class='f_c']/div/div/a[1]/@href")[0])
    elif len(html.xpath("//td[@class='t_f']//a/@href")) != 0:  # 第二种获取方式
        # 查看获取的链接列表，如果只有第一个，则取第一个链接，如果是两个，取第二个链接
        if len(html.xpath("//td[@class='t_f']//a/@href")) == 2:  # 获取的是第二个链接
            seed_page_address.append(addr_title + html.xpath("//td[@class='t_f']//a/@href")[1])
            seed_file_address.append(etree.HTML(get_url(seed_page_address[0]).text).
                                     xpath("//body/div[@class='wp']/div[@class='f_c']/div/div/a[1]/@href")[0])  # 链接地址列表
        else:  # 第三方网站存储的种子信息
            if html.xpath("//td[@class='t_f']//a/@href")[0].startswith("http"):
                seed_page_address.append(html.xpath("//td[@class='t_f']//a/@href")[0])
            else:
                seed_page_address.append(addr_title + html.xpath("//td[@class='t_f']//a/@href")[0])
            seed_file_address_1 = etree.HTML(get_url(seed_page_address[0]).text). \
                xpath("//input[@id='btnDownload']")  # 链接地址列表
            s = etree.tostring(seed_file_address_1[0], encoding="utf-8", pretty_print=True, method="html").decode(
                "utf-8")
            seed_file_address.append(addr_title + etree.HTML(s).xpath('//@onclick')[0].split("'")[-2])
    else:
        pass
    return seed_page_address, seed_file_address


def delete_empty_files(root_path):
    all_file_list = tools.get_all_files(root_path)
    for path in all_file_list:
        print(path)
        if tools.is_or_not_file(path):
            print("文件{}".format(path))
            if len(tools.read_file(path, "rb")) == 0:
                os.remove(path)
                print("删除文件{}".format(path))
