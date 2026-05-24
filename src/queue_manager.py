import queue
import threading
import time


class queue_manager:
    def __init__(self):
        self.crawl_delay = 0
        self.request_rate = 0
        self.page_queue = queue.Queue()
        self.img_queue = queue.Queue()
        self.vid_queue = queue.Queue()
        self.txt_queue = queue.Queue()
        self.last_request = 0
        self.lock = threading.Lock()

    def queue_to_list(self):
        urls = []
        imgs = []
        vids = []
        for i in range(self.page_queue.qsize()):
            url = self.page_queue.get()
            urls.append(url)

        for i in range(self.img_queue.qsize()):
            img = self.img_queue.get()
            imgs.append(img)

        for i in range(self.vid_queue.qsize()):
            vid = self.vid_queue.get()
            vids.append(vid)

        return urls, imgs, vids

    def put_item(self, **kwargs):
        page_list = kwargs.get("page_list", [])
        img_list = kwargs.get("img_list", [])
        vid_list = kwargs.get("vid_list", [])

        if len(page_list) > 0:
            for u in page_list:
                self.page_queue.put(u)

        if len(img_list) > 0:
            for u in img_list:
                self.img_queue.put(u)
        if len(vid_list) > 0:
            for u in vid_list:
                self.vid_queue.put(u)

    def delay_counter(self) -> None:
        while True:
            with self.lock:
                agora = time.perf_counter()
                t = agora - self.last_request
                bl = t >= self.crawl_delay
                if bl:
                    self.last_request = time.perf_counter()
                    return
            time.sleep(0.1)

    def add_delay(self, delay):
        self.crawl_delay += delay

    def get_url(self):
        self.delay_counter()

        item = self.page_queue.get()
        return item

    def get_file(self):
        while True:
            self.delay_counter()
            yield self.img_queue.get(), "img"
            self.delay_counter()
            yield self.vid_queue.get(), "vid"
