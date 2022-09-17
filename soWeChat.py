from selenium import webdriver
import requests
import time
from lxml import etree
from bs4 import BeautifulSoup
import random, json


# get cookie
def get_cookies():
    driver = webdriver.Chrome()
    driver.get("http://weixin.sogou.com/")

    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    time.sleep(10)

    cookies = driver.get_cookies()
    print(cookies)
    cookie = {}
    for items in cookies:
        cookie[items.get('name')] = items.get('value')
    return cookie


# get total page num
def get_page_links(search, cookie, header):
    # example
    # result = etree.tostring(html)
    # print(result.decode('utf-8'))

    page_source = requests.get("http://weixin.sogou.com/weixin?query=%s&type=2&page=1" % search, cookies=cookie,
                               headers=header)
    print(page_source)


# get all article links
def get_links(page_count, search, cookie, header, available_proxy):
    # if page_count = 100

    number = 0
    for i in range(page_count):
        num = i + 80
        flag = True
        # while (flag):
        page_source = requests.get("http://weixin.sogou.com/weixin?query=%s&type=2&page=%s" % (search, num),
                                   cookies=cookie, headers=header).content
        # , proxies = available_proxy[random.randint(0, len(available_proxy))]
        bs_obj = BeautifulSoup(str(page_source, encoding="utf-8"), "html.parser")
        url_list = bs_obj.findAll("div", {"class": "txt-box"})
        # if len(url_list):
        #     flag = True
        # else:
        #     flag = False
        # put article links into a list
        final_url_list = []

        for url in url_list:
            link = url.h3.a.attrs['href']
            final_url_list.append(link)

        number = number + len(url_list)
        print(number)

        time.sleep(3)

        with open("data/articleLinks3.txt", 'a+', encoding="utf-8") as f:
            f.writelines(line + '\n' for line in final_url_list)

    # return final_url_list


if __name__ == "__main__":
    # init header
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    }
    with open("data/available_proxy.txt", "r", encoding="utf-8") as f:
        proxies = f.readlines()

    proxies = [eval(i.strip("\n")) for i in proxies]

    # get article links function
    cookies = get_cookies()
    get_links(30, "孟晚舟", cookies, headers, proxies)
