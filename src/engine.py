import os
import requests

from urllib.parse import urlparse
from pathlib import Path

import src.network_manager as nm
import src.ThreadManager as tm
import src.queue_manager as qm
import src.storage_handler as sh
import src.OldManager as oh
import src.utils as u

ENCODING = "utf-8"


class engine:
    def __init__(
        self,
        url: str,
        config: dict,
        isolation: bool,
        load: bool,
        ua,
        callback_func=None,
    ):

        self.callback = callback_func
        self.load_bool = load
        self.session = requests.Session()
        self.cfg = config
        self.isolation = isolation
        self.ua = ua
        self.url_inicial = url
        self.threads = tm.ThreadManager(self.cfg["threads"])
        self.queue = qm.queue_manager()
        self.page_old = oh.OldManager(
            path=self.cfg["path"], name_file="page_old"
        )
        self.img_old = oh.OldManager(self.cfg["path"], "img_old")
        self.vid_old = oh.OldManager(self.cfg["path"], "vid_old")
        self.log_cache = []
        self.stats_data = set()
        self.count_down = 0
        self.count_url = 0

    # regula o delay entre requisicoes caso retorne code 429
    def request_code_manager(self, code: int):
        if code == 429:
            self.queue.add_delay(0.1)
            self.add_log(
                "[WARN]Requisicao Bloqueada por excesso de requisicoes"
            )

    def add_log(self, text: str) -> None:
        self.log_cache.append(u.log_Manager(text))

    # inicia o codigo principal do scrapper
    def start(self) -> None:
        self.add_log("[INFO]Engine Iniciada ")

        infos = nm.verify_robot(
            self.url_inicial,
            self.session,
            self.url_inicial,
            self.ua,
            self.isolation,
        )

        self.queue.put_item(page_list=[infos["url"]])

        self.request_code_manager(infos["code"])
        qm.crawl_delay = infos["cd"]

        self.threads.create_threads(
            func=self.manager_list,
            list_thr=self.threads.thr_url,
            name="tu_",
        )
        self.threads.create_threads(
            func=self.download,
            list_thr=self.threads.thr_down,
            name="td_",
            path=self.cfg["path"],
        )

        self.threads.start_thr()
        self.threads.join_thr()

    # comeca capturar as urls
    def manager_list(self, **kwargs) -> None:
        while True:

            url = self.queue.get_url()
            self.count_url += 1
            infos = nm.verify_robot(
                self.url_inicial, self.session, url, self.ua, self.isolation
            )

            self.add_log(infos["msg"])
            self.request_code_manager(infos["code"])
            if self.page_old.verify(url):
                self.page_old.add_item(url)
                if infos["permission"]:
                    up = urlparse(url)
                    html = self.session.get(url, headers=self.ua)
                    msg, page_new, img_new, vid_new = nm.get_url(
                        up.scheme, up.netloc, html
                    )
                    self.add_log(msg)
                    self.queue.put_item(
                        page_list=page_new, img_list=img_new, vid_list=vid_new
                    )
                    img_new.clear()
                    page_new.clear()
                    vid_new.clear()
                    self.call_back()

                    if self.queue.page_queue.qsize() == 0:
                        self.add_log("[WARN]Sem Mais Urls para Processar")

    def call_back(self):
        if self.callback:
            concluida, pendente, total = self.att_var()
            message = self.log_cache
            threads_info = self.threads.get_info()
            self.callback(concluida, pendente, total, message, threads_info)
            self.log_cache.clear()

    # realiza o download dos arquivos
    def download(self, **kwargs) -> None:
        path = kwargs["path"]
        path = Path(path)

        while True:
            get = self.queue.get_file()
            url, tipo = next(get)

            if self.img_old.verify(url):
                name_file = nm.find_name(url)
                response = self.session.get(url, headers=self.ua)
                code = response.status_code

                if code == 404:
                    self.add_log(f"[INFO]Pagina retornou 404:{url}")
                    if tipo == "img":
                        self.img_old.add_item(url)
                        pass
                    elif tipo == "vid":
                        self.vid_old.add_item(url)
                        pass

                else:
                    self.count_down += 1
                    try:
                        self.request_code_manager(code)
                        sh.save_file(name_file, path, response)
                    except Exception as e:
                        self.add_log(f"[WARN]Exception : {e}")
                    if tipo == "img":
                        self.img_old.add_item(url)
                    elif tipo == "vid":
                        self.vid_old.add_item(url)

                if self.queue.img_queue.qsize() == 0:
                    self.add_log("[INFO]Sem Mais Arquivos para baixar")

    def quit(self):
        self.save()
        os.system("exit")

    def load(self):
        if self.load_bool:
            self.add_log("[INFO]Carregando Urls Salvas")
            url = sh.load_url(self.cfg["path"], "url_save")
            img = sh.load_url(self.cfg["path"], "img_save")
            vid = sh.load_url(self.cfg["path"], "vid_save")

            self.page_old.list_old = sh.load_url(self.cfg["path"], "url_old")
            self.page_old.list_old = sh.load_url(self.cfg["path"], "img_old")
            self.page_old.list_old = sh.load_url(self.cfg["path"], "vid_old")

            self.queue.put_item(page_list=url, img_list=img, vid_list=vid)

            if self.callback:
                c, p, t = self.att_var()
                m = self.log_cache
                self.callback(c, p, t, m)

    def save(self):
        urls, imgs, vids = self.queue.queue_to_list()
        log = []
        log.append(sh.save_csv_url(urls, self.cfg["path"], "url_save"))
        log.append(sh.save_csv_url(imgs, self.cfg["path"], "img_save"))
        log.append(sh.save_csv_url(vids, self.cfg["path"], "vid_save"))

        log.append(
            sh.save_csv_url(
                self.page_old.list_old, self.cfg["path"], "url_old"
            )
        )
        log.append(
            sh.save_csv_url(self.img_old.list_old, self.cfg["path"], "img_old")
        )
        log.append(
            sh.save_csv_url(self.vid_old.list_old, self.cfg["path"], "vid_old")
        )
        for log_message in log:
            self.add_log(log_message)
        if self.callback:
            conclusion, pending, total = self.att_var()
            log = self.log_cache
            self.callback(conclusion, pending, total, log)

    # atualiza as variaveis para enviar para a interface atravez de message
    # do textual
    def att_var(self):
        concluida = {
            "urls": self.page_old.count_list(),
            "imgs": self.img_old.count_list(),
            "vids": self.vid_old.count_list(),
            "txt": 0,
        }
        pendente = {
            "urls": self.queue.page_queue.qsize(),
            "imgs": self.queue.img_queue.qsize(),
            "vids": self.queue.vid_queue.qsize(),
            "txt": 0,
        }

        total = {
            "urls": self.page_old.count_list() + self.queue.page_queue.qsize(),
            "imgs": self.img_old.count_list() + self.queue.img_queue.qsize(),
            "vids": self.vid_old.count_list() + self.queue.vid_queue.qsize(),
            "txt": 0,
        }
        return concluida, pendente, total

    def rate_value(self):
        down = self.count_down
        url = self.count_url
        self.count_url = 0
        self.count_down = 0
        return down, url
