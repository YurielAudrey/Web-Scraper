import requests
from bs4 import BeautifulSoup as s
class ws:
    def __init__(self,url_inicial="",qtd=0):
        self.url_inicial = url_inicial
        self.qtd = qtd
        self.encode = "utf-8"

    def down_img(self,img_url):
        count = 0
        for url in img_url:
            response = requests.get(url)
            with open(f"image_{count}","wb") as f:
                f.write(response.content)
            count =+ 1

    def scrapper(self,url,ua):
        code, html = self.get_html(url, ua)
        page_url, img_url = self.get_url(html)
        return code,html,page_url,img_url

    def start_new(self,url_inicial,ua):
        code,html,page_url,img_url = self.scrapper(url_inicial,ua)


        list_old = []
        for url in page_url:
            if url=="":
                page_url.pop(0)
                pass
            self.scrapper(url,ua)
            list_old.append(url)
            page_url.remove(url)

        self.save_url(page_url,"url.csv")
        self.save_url(list_old, "list_old.csv")

    def get_html(self,url,user_agent):
        html = requests.get(url,headers = user_agent)
        code = html.status_code
        return code , html

    #arrumar , ja que isso so fix url proveniente do wikipedia , manter ele de forma generica
    def fix_url(self,u):
        url = u
        if u == None:
            return "null"
        if url.startswith("https://") or url.startswith("http://") :
            return url
        else : return "null"



    #vasculha o html em busca de links
    def get_url(self,html):

        page_url = []
        img_url = []
        soup = s(html.text,'html.parser')

        for tag_img in soup.find_all('img'):
            img = tag_img.get('src')
            img_fixed = self.fix_url(img)
            if img_fixed == "null":
                img_fixed =""
            img_url.append(img_fixed)

        for tag_a in soup.find_all('a'):
            url = tag_a.get('href')
            url_fixed = self.fix_url(url)
            if url_fixed == "null":
                url_fixed = ""
            page_url.append(url_fixed)

        page_clear = list(filter(None, page_url))
        img_clear = list(filter(None, img_url))
        return page_clear,img_clear



    #transforma a lista em csv
    def save_url(self,page_url,arquivo):
        with open(arquivo,"w",encoding=self.encode) as f:
            count = 0
            for url in page_url:
                if count == 0: pre_save = url
                else :pre_save = f"{pre_save},{url}"
                count =+ 1

            f.write(f"{pre_save}")
        f.close()

    def load_url(self,arquivo):
        with open(arquivo,"r",encoding=self.encode)as f:
            url_list = f.read().split(",")
        f.close()
        return url_list



#
#
#
#
#
#
#
#
#
#
#
#
#
