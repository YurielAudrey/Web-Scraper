from bs4 import BeautifulSoup as s
from urllib.parse import urlparse
from pathlib import Path


from src import utils as pu


# captura todas as Url no HTMl
def get_url(scheme, netloc, html):

    page_url = []
    img_url = []
    vid_url = []
    soup = s(html.text, "html.parser")
    url = ""
    tipo = ""
    try:
        for tag in soup.find_all(["img", "a", "video"]):
            if tag.name == "a":
                url = tag.get("href")
                tipo = "link"
            elif tag.name == "img":
                url = tag.get("src")
                tipo = "img"
            elif tag.name == "video":
                url = tag.get("src")
                tipo = "vid"

            if url:
                url_fixed = pu.fix_url(scheme, netloc, url)
                if url_fixed == "null":
                    url_fixed = ""

                if tipo == "link":
                    page_url.append(url_fixed)
                elif tipo == "img":
                    img_url.append(url_fixed)
                elif tipo == "vid":
                    vid_url.append(url_fixed)

        page_clear = list(set(filter(None, page_url)))
        img_clear = list(set(filter(None, img_url)))
        vid_clear = list(set(filter(None, vid_url)))

        return "", page_clear, img_clear, vid_clear
    except Exception as e:
        msg = f"[WARN][Get URL] Exception:{e}"  # apagar
        return msg, [], [], []


# Captura o nome do arquivo
def find_name(url: str) -> str:
    parsed_url = urlparse(url)
    path_file = parsed_url.path
    name_file = Path(path_file).name
    return name_file
