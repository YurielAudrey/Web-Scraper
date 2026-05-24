from textual.message import Message


class UiUpdate(Message):
    def __init__(
        self,
        concluida: dict,
        pendente: dict,
        total: dict,
        msg: str,
        threads_info,
    ):

        self.concluida: dict = concluida
        self.pendente: dict = pendente
        self.total: dict = total
        self.log: str = msg
        self.threads_info: dict = threads_info

        super().__init__()
