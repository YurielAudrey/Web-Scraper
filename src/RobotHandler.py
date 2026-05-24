from urllib.parse import urlparse
from pathlib import Path
from protego import Protego

class RobotHandler:
    def __init__(self,url_inicial,ua,session,isolation):
        self.ua = ua
        self.session = session
        self.isolation = isolation
        self.url_inicial = url_inicial
        self.infos = {
            "url": '',
            "msg": "",
            "cd": 0,
            "permission": '',
            "code": '',
        }



    def verify_robot(self, url):

        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            response = self.session.get(base_url, headers=self.ua)
            code = response.status_code
            rp = Protego.parse(response.text)
            permission = rp.can_fetch(url, self.ua)
            cd = rp.crawl_delay(self.ua)
            infos = {
                "url": url,
                "msg": "",
                "cd": cd,
                "permission": permission,
                "code": code,
            }



    #implementar isolation
    #implementar permissao