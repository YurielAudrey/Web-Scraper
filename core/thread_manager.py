import threading as thr


class Threads:
    def __init__(self, t_number):
        self.thread_n = t_number
        self.thr_url = []
        self.thr_down = []

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
