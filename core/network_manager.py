from bs4 import BeautifulSoup as s
from urllib.parse import urlparse
from pathlib import Path
from protego import Protego

from core import utils as pu


def verify_robot(url_inicial, session, url, header, isolation):

    ui = urlparse(url_inicial)
    parsed_url = urlparse(url)
    ua = header["User-Agent"]
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    response = session.get(base_url, headers=header)
    code = response.status_code
    rp = Protego.parse(response.text)
    permission = rp.can_fetch(url, ua)
    cd = rp.crawl_delay(ua)
    infos = {
        "url": url,
        "msg": "",
        "cd": cd,
        "permission": permission,
        "code": code,
    }
    if isolation:
        if parsed_url.netloc != ui.netloc:
            msg = f"[WARN] Sistema de Isolamento bloqueou "
            return infos

    if permission:
        return infos
    else:
        msg = f"[WARN] Permissao Negada para o Site {url}"
        infos["msg"] = msg
        return infos


# captura todas as Url no HTMl
def get_url(scheme, netloc, html):

    page_url = []
    img_url = []
    vid_url = []
    soup = s(html.text, "html.parser")
    url = ""
    tipo = ""

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
        elif tag.name == "text":
            pass

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
    msg = f"[INFO] adcionando URLS a lista "
    return msg, page_clear, img_clear, vid_clear


# Captura o nome do arquivo
def find_name(url: str) -> str:
    parsed_url = urlparse(url)
    path_file = parsed_url.path
    name_file = Path(path_file).name
    return name_file
