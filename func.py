import os
from time import sleep
import requests
from bs4 import BeautifulSoup as s
import pyfiglet




def get_html(url,user_agent):
    html = requests.get(url,headers = user_agent)
    code = html.status_code
    return code , html


def fix_url(u):
    url = u
    if url.startswith("//"):
        url ="https:"+url
    elif url.startswith("#"):
        url = ""
    elif url.startswith("/wiki") or url.startswith("/w/") :
        url = "https://pt.wikipedia.org/"+url
    else :
        return url
    return url

def get_url(html):

    page_url = []
    img_url = []
    soup = s(html.text,'html.parser')
    for tag_img in soup.find_all('img'):
        img = tag_img.get('src')
        img_fixed = fix_url(img)
        img_url.append(img_fixed)
    for tag_a in soup.find_all('a'):
        url = tag_a.get('href')
        url_fixed = fix_url(url)
        page_url.append(url_fixed)
    return page_url , img_url

def save_url(page_url):
    with open("url_list.txt","w",encoding="utf-8") as f:
        for url in page_url:
            f.write(f"{url}\n")
    f.close()
def save_old(url_old):
    with open ("url_old.txt","a",encoding="utf-8") as f:
        f.write(f"{url_old}\n")
