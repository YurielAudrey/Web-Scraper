import os
from time import sleep
import requests
from bs4 import BeautifulSoup as s

url_inicial = "https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal"
delay = 1
ua = {"User-Agent": "Python/3.14"}


def get_html(url,user_agent):
    html = requests.get(url,headers = user_agent)
    print(html.status_code)
    return html


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

html = get_html(url_inicial,ua)
page_url,img_url = get_url(html)
save_url(page_url)
