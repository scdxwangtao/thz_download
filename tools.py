import shutil
import os
from fake_useragent import UserAgent
import requests
import http.client


def mkdir(path, is_delete=False):
    """
    Method to create a new subdirectory
    :param is_delete: Whether or not to delete
    :param path:  The address to create the folder
    :return: Boolean
    """
    # Remove the leading space and then the trailing \ symbol.
    path = path.strip().rstrip("\\")

    # Check whether a path exists。True for existence and False for nonexistence.
    is_exists = os.path.exists(path)

    if not is_exists:
        # If the directory address does not exist, create the directory.
        try:
            os.makedirs(path)
            print("directory:" + path + ' Creating a successful!')
            return True
        except Exception as e:
            print("directory:" + path + ' Create a failure！')
            print(e)
            return False
    else:
        # If the directory exists, it is not created and a message
        # is displayed indicating that the directory already exists.
        print("directory:" + path + ' the directory already exists, delete the original directory and '
                                    'create a new directory.')
        try:
            # delete the original directory.
            if is_delete:
                shutil.rmtree(path)
                print("The original directory has been deleted.")
                # Create the directory again.
                try:
                    os.makedirs(path)
                    print("directory:" + path + ' Succeeded in creating the directory again!')
                    return True
                except Exception as e:
                    print("directory:" + path + ' Failure in creating the directory again！')
                    print(e)
                    return False
        except Exception as e:
            print("Failed to delete the original directory.")
            print(e)


def get_url(url, referer=None):
    """
    Method to get the response page
    :param url: indicates the address of the page to be obtained.
    :param referer: The HTTP Referer is part of the header. When a browser sends a request to a Web server,
            it usually carries the Referer with it to tell the server from which page the web page is linked,
            so that the server can obtain some information for processing.
    :return response the retrieved response content.
    """
    # Random generation User-Agent
    ua = UserAgent()
    headers = {'User-Agent': ua.random, "Referer": referer}
    # stream=True   requests.exceptions.ChunkedEncodingError:
    # ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))
    response = requests.get(url, headers=headers, stream=True)
    return response


def update_name(name):
    """
    The method of updating the name
    :param name: The name you want to change.
    :return: Modified name
    """
    string = "~`!@#$%^&*()+-/=|\\[]{};:'\"<,>.?"
    # Check if the string contains any of the special symbols listed above and replace them with "_"
    for i in string:
        if i in name:
            name = name.replace(i, "_")     # Replace special characters
    return name


def save_image(path, img_s_url, name, j):
    """
    Save the picture method, need to pass in the picture serial number
    :param path: save path
    :param j: image number
    :param img_s_url: image url address
    :param name: save name
    :return: Boolean
    """
    r = get_url(img_s_url)
    print("Start saving image information to file directory: " + name + "_{}.jpg".format(j + 1))
    with open(path + name + "_{}.jpg".format(j + 1), 'wb')as f:
        f.write(r.content)
        print("Description Saving the image information to the directory succeeded.")
        return f.closed


def save_seed_file(path, seed_file_address, numb, name, referer=None):
    """
    Method of saving seed files
    :param path: Save path
    :param seed_file_address:   Seed file address
    :param numb: Save file name
    :param name: Save file name
    :param referer: http header parameter
    :return: Boolean
    """
    r = get_url(seed_file_address, referer)
    print("Start saving the seed file.  \r\nFile name is:  " + name + "_{}.torrent".format(numb))
    with open(path + name + "_{}.torrent".format(numb), "wb") as f:
        f.write(r.content)
        print("The seed file is saved successfully.")
    return f.closed


def count_lines(file_path):
    """
    Gets the number of lines of the current file by passing in the file address
    :param file_path:
    :return:
    """
    count = -1
    for count, line in enumerate(open(file_path, 'rU')):
        pass
    count += 1
    return count


def read_file(path, types):
    """

    :param path: fire path
    :param types: "r" or "rb"
    :return: list
    """
    with open(path, types) as r:
        return r.readlines()


def get_all_files(path):
    """
    Get all the addresses
    :param path:    root path
    :return: all file path and name
    """
    all_file = []
    for dir_path, dir_names, filenames in os.walk(path):
        for dir_ in dir_names:
            all_file.append(os.path.join(dir_path, dir_))
        for name in filenames:
            all_file.append(os.path.join(dir_path, name))
    return all_file


def is_or_not_file(path):
    """
    Method to determine if it is a file
    :param path: file or dir path
    :return:  True is File False is dir
    """
    return os.path.isfile(path)
