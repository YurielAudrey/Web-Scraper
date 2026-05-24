import threading as thr


class ThreadManager:
    def __init__(self, t_number):
        self.thread_n: int = t_number
        self.thr_url: list[thr.Thread] = []
        self.thr_down: list[thr.Thread] = []
        self.threads_info: list[dict] = []

    def create_threads(self, func, name, *args, **kwargs):
        list_thread = kwargs.get("list_thr")
        for x in range(self.thread_n):
            list_thread.append(
                thr.Thread(
                    name=f"{name}{x}", target=func, args=args, kwargs=kwargs
                )
            )
        return list_thread

    def start_thr(self):
        for t in range(self.thread_n):
            self.thr_down[t].start()
            self.thr_url[t].start()

    def join_thr(self):
        for t in range(self.thread_n):
            self.thr_down[t].join()
            self.thr_url[t].join()

    def set_info(self, thr_list: list, categoria: str):

        for thread in thr_list:
            thr_id = thread.native_id
            thr_name = thread.name

            status = thread.is_alive()
            info = {
                "id": thr_id,
                "name": thr_name,
                "Categoria": categoria,
                "status": status,
            }
            self.threads_info.append(info)

    def get_info(self):
        self.threads_info.clear()
        self.set_info(self.thr_url, "URL Scrapper")
        self.set_info(self.thr_down, "Download File")

        return self.threads_info
