import time
from multiprocessing.pool import ThreadPool

import tools
from detail_page import get_detail_page
import threadpool


def detail_pool(forum_name, func_name, thread_num):
    """线程池的使用"""
    pool = threadpool.ThreadPool(thread_num)
    list_urls = tools.read_file(forum_name + "_detail.txt", "r")
    print(len(list_urls))
    for i in range(len(list_urls)):
        requests = threadpool.makeRequests(func_name, [([], {"url": list_urls[i]})])
        [pool.putRequest(req) for req in requests]
    pool.wait()


def get_image_pool(func_name, thread_num, img_s):
    """线程池的使用"""
    pool = threadpool.ThreadPool(thread_num)
    for i in range(len(img_s)):
        requests = threadpool.makeRequests(func_name, [([], {"img_s_url": img_s[i]})])
        [pool.putRequest(req) for req in requests]
    pool.wait()

