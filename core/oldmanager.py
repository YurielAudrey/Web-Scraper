import core.storage_handler as sh


class OldManager:
    def __init__(self, path: str, name_file: str):
        self.name_file = name_file
        self.list_old = []

    def verify(self, url: str) -> bool:
        for u in self.list_old:
            if u == url:
                return False
        return True

    def add_item(self, url: str) -> None:
        if self.verify(url):
            self.list_old.append(url)

    def save_old(self, path):
        sh.save_csv_url(self.list_old, path, self.name_file)

    def count_list(self):
        return len(self.list_old)
