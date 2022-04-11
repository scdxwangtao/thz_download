# 引入模块
import time

import requests
from lxml import etree

import logical_page
import tools


def get_detail_page(url):
    """
    By passing in links to detailed pages, parse and save the information you need.
    :param url: Detail page url.
    :return:
    """
    print("Start retrieving page details for parsing based on the current URL......")
    print("The url currently parsed is:  " + url)

    addr_title = url.split("/")[0] + "//" + url.split("/")[2] + "/"           # Get home page address
    print("Home page address： " + addr_title)

    page = tools.get_url(url)
    if page.status_code == 200:
        html = etree.HTML(page.text)                  # Add the retrieved page content to xpath.
        text = html.xpath("//div[contains(@class,'t_fsz')]/table")  # Gets part of the details page.
        name = html.xpath('//*[@id="thread_subject"]/text()')[0]      # Gets the save name.
        forum_name = tools.update_name(html.xpath("//div[@class='bm cl']//a[4]/text()")[0])
        print("forum name: " + forum_name)
        secondary_classification = tools.update_name(html.xpath(
            "//h1[@class='ts']//a/text()")[0].rstrip("]").lstrip("["))
        print("secondary classification:  " + secondary_classification)
        name = tools.update_name(name)                           # Example Modify the name of an invalid file.
        print("movie_name:  " + name)

        '''Create the current name folder under the Data folder.'''
        # Create a level 1 plate directory
        tools.mkdir("data/" + forum_name)
        # Create a secondary plate directory
        tools.mkdir("data/" + forum_name + "/" + secondary_classification)
        # Create a directory for saving files
        tools.mkdir("data/" + forum_name + "/" + secondary_classification + "/" + name, True)
        path = "data/" + forum_name + "/" + secondary_classification + "/" + name + "/" + name
        '''Save movie information.'''
        logical_page.save_movie_information(path, text, name, url)

        '''Save images.'''
        logical_page.parse_save_image(path, html, addr_title)

        '''Gets the address of the magnetic link,Determine the location of the seed file link.'''
        parse_tup = logical_page.parse_seed_file_address(html, addr_title)
        if len(parse_tup[0]) != 0:
            for i in range(len(parse_tup[0])):
                print("seed page address： " + parse_tup[0][i])
                print("seed file address： " + parse_tup[1][i])

        '''Save the seed file according to the seed file address.'''
        # Because the seed file link is anti-spoofed, you need to pass the Referer parameter in the request header,
        # which is the address above the seed link.
        if len(parse_tup[0]) != 0:
            for i in range(len(parse_tup[0])):
                tools.save_seed_file(path, parse_tup[1][i], i + 1, name, parse_tup[0][i])  # referer

        print("The detailed information on the current page is successfully resolved......")



