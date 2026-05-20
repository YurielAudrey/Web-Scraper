from jedi.api import classes
from textual.screen import Screen
from textual import on, work
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Rule, Label, DataTable, RichLog

from core import UiUpdate as uup
from core import engine as e


class ProcessScreen(Screen):
    def __init__(self, url, cfg, isolation, load=False):
        super().__init__()
        self.url = url
        self.cfg = cfg
        self.isolation = isolation
        self.load = load
        self.engine_inst = None
        self.infos = {
            "Email": self.cfg["email"],
            "Threads": self.cfg["threads"],
            "Isolamento": self.isolation,
            "Path": self.cfg["path"],
            "Url Inicial": self.url,
        }

    BINDINGS = [
        ("ctrl+s", "save_quit", "salvar e fechar"),
        ("ctrl+p", "pause", "pausar"),
    ]

    CSS_PATH = "../css/processPage.tcss"

    def compose(self):

        yield Header()
        with Horizontal(classes="tables-container") as tables:
            tables.border_title = "Tables"
            yield DataTable(id="info_table", classes="info-table")
            yield DataTable(id="down_table", classes="down-table")

        with Horizontal(classes="thr-container") as threads:
            container_1 = Horizontal(
                DataTable(id="url_threads", classes="threads_table"),
                classes="threads-container",
            )
            container_1.border_title = "Threads url"
            container_2 = Horizontal(
                DataTable(id="down_threads", classes="threads_table"),
                classes="threads-container",
            )
            container_2.border_title = "Threads Downloads"

            yield container_1
            yield container_2
        with Horizontal(classes="log-container") as log:
            log.border_title = "Log"
            yield RichLog(
                classes="log", auto_scroll=True, highlight=True, markup=True
            )

        yield Footer()

    # cria as colunas e linhas da tabela
    def on_mount(self) -> None:

        down = self.query_one("#down_table", DataTable)
        down.add_column("Type", key="type")
        down.add_column("Concluida", key="ok")
        down.add_column("Restante", key="rest")
        down.add_column("Total", key="total")
        rows = {
            "URL": "row_url",
            "imagens": "row_img",
            "videos": "row_vid",
        }
        for label, value in rows.items():
            down.add_row(label, "0", "0", "0", key=value)

        info = self.query_one("#info_table", DataTable)
        info.add_column("Descricao", key="Desc")
        info.add_column("Value", key="value")
        for label, value in self.infos.items():
            info.add_row(label, value)

        self.start_run()

    def action_save_quit(self) -> None:
        self.engine_inst.quit()

    def action_pause(self) -> None:
        pass

    @work(thread=True)
    def start_run(self):
        title = "Horus"
        version = "1.0"

        github_url = "https://github.com/YurielAudrey/Horus"
        ua = {
            "User-Agent": f"{title}/{version} ({github_url};"
            f" {self.cfg['email']})"
            "Request/2.32.5"
        }

        def update_ui(p, r, t, m):
            self.post_message(uup.UiUpdate(p, r, t, m))

        self.engine_inst = e.engine(
            self.url, self.cfg, self.isolation, self.load, ua, update_ui
        )
        self.engine_inst.start()

    @on(uup.UiUpdate)
    def atualizar_labels(self, message: uup.UiUpdate):
        log = self.query_one(RichLog)
        tipos = {
            "urls": "row_url",
            "imgs": "row_img",
            "vids": "row_vid",
        }

        for i in message.log:
            if i != "":
                log.write(i)

        for key_engine, key_tabela in tipos.items():
            table = self.query_one("#down_table", DataTable)

            valor_concluido = message.concluida.get(key_engine, [])
            valor_pendente = message.pendente.get(key_engine, 0)
            valor_total = message.total.get(key_engine, 0)

            table.update_cell(key_tabela, "ok", str(valor_concluido))
            table.update_cell(key_tabela, "rest", str(valor_pendente))
            table.update_cell(key_tabela, "total", str(valor_total))
