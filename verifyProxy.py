import requests
import iptools
from bs4 import BeautifulSoup as Soup

# verify the ip availability
def verifyFunc(url, proxy):
    r = requests.get(url, proxies=proxy)
    return r.status_code


# read proxy ip
def get_ProxyByFile():
    # verify url address
    url_address = "https://www.baidu.com"

    with open("data/download.txt", "r", encoding="utf-8") as f:
        proxys = f.readlines()
    proxys = [i.strip("\n") for i in proxys]

    # available proxy
    available_proxy = []

    for item in proxys:
        proxy_dict = {
            "https": ''.join(("https://", item))
        }
        print(proxy_dict)
        status = verifyFunc(url_address, proxy_dict)
        if status == 200:
            print("available proxy: %s" % str(proxy_dict))
            available_proxy.append(proxy_dict)
        else:
            continue

    with open("data/available_proxy.txt","w",encoding="utf-8") as f:
        f.writelines(str(line) + '\n' for line in available_proxy)

    return available_proxy


# crawl proxy
def crawl_proxy():
    pass



if __name__ == "__main__":
    get_ProxyByFile()
