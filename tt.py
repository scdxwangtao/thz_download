import os


def test_readfile(filepath):
    """
    :param filepath:
    :return:
    """
    with open(filepath, "r") as r:
        return r.readlines()


# def getallfiles(path):
#     allfile=[]
#     for dirpath, dirnames, filenames in os.walk(path):
#         for dir in dirnames:
#             allfile.append(os.path.join(dirpath,dir))
#         for name in filenames:
#             allfile.append(os.path.join(dirpath, name))
#     return allfile
#
#
# if __name__ == '__main__':
#     path = "D:\qycache"
#     allfile = getallfiles(path)
#     for file in allfile:
#         print(file)


if __name__ == '__main__':
    path = "2020_09_28 桃花族无毛宣言177GB合集2020_09_28 桃花族无毛宣言177GB合集_2.jpg"
    print(test_readfile(path))
    if len(test_readfile(path)) == 0:  # 空文件，删除
        os.remove(path)
