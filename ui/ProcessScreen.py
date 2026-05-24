import asyncio
import time

from textual_plotext import PlotextPlot
from textual.errors import TextualError
from textual.screen import Screen
from textual import on, work
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Rule, Label, DataTable, RichLog
from textual.widgets.data_table import (
    CellDoesNotExist,
    RowDoesNotExist,
    ColumnDoesNotExist,
)


from src import UiUpdate as uup
from src import engine as e


class ProcessScreen(Screen):
    def __init__(self, url, cfg, isolation, load=False):
        super().__init__()
        self.url = url

        self.cfg = cfg
        self.isolation = isolation
        self.load = load
        self.engine_inst: e.engine
        self.historico_x = []
        self.historico_down = []
        self.historico_url = []
        self.infos = {
            "Email": self.cfg["email"],
            "Threads": self.cfg["threads"],
            "Isolamento": self.isolation,
            "Path": self.cfg["path"],
            "Url Inicial": self.url,
        }
        title = "Horus"
        version = "1.0"

        github_url = "https://github.com/YurielAudrey/Horus"
        ua = {
            "User-Agent": f"{title}/{version} ({github_url}; {self.cfg['email']})Request/2.32.5"
        }

        def update_ui(concluida, pendente, total, message, threads):
            self.post_message(
                uup.UiUpdate(concluida, pendente, total, message, threads)
            )

        self.engine_inst = e.engine(
            self.url, self.cfg, self.isolation, self.load, ua, update_ui
        )
        self.columns_threads = {}
        self.set_interval(2.0, self.prot)

    BINDINGS = [
        ("ctrl+s", "save_quit", "salvar e fechar"),
        ("ctrl+p", "pause", "pausar"),
    ]

    CSS_PATH = "../css/processPage.tcss"

    def compose(self):

        yield Header()
        with Horizontal(classes="tables") as tables:
            tables.border_title = "Tables"
            container_t = Horizontal(
                DataTable(id="info_table", classes="info-table"),
                classes="tables_container",
            )
            container_t.border_title = "infos"
            yield container_t
            container_d = Horizontal(
                DataTable(id="down_table", classes="down-table"),
                classes="tables_container",
            )
            container_d.border_title = "Processados"
            yield container_d
        with Horizontal(classes="thr-container") as threads:
            container_1 = Horizontal(
                DataTable(id="threads_table", classes="threads_table"),
                classes="threads-container",
            )
            container_1.border_title = "Threads"
            container_2 = Horizontal(
                PlotextPlot(id="plt", classes="plotext"),
                classes="prot-container",
            )
            container_2.border_title = "Graphic"

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
        down_rows = {
            "URL": "row_url",
            "imagens": "row_img",
            "videos": "row_vid",
        }
        for label, value in down_rows.items():
            down.add_row(label, "0", "0", "0", key=value)

        info = self.query_one("#info_table", DataTable)
        info.add_column("Descricao", key="Desc")
        info.add_column("Value", key="value")
        for label, value in self.infos.items():
            info.add_row(label, value)

        threads = self.query_one("#threads_table", DataTable)
        self.columns_threads = {
            "id": "id_column",
            "Name": "name_column",
            "Categoria": "cat_column",
            "Status": "status_column",
        }
        for label, value in self.columns_threads.items():
            threads.add_column(label, key=value)

        self.start_run()

    def action_save_quit(self) -> None:
        self.engine_inst.quit()

    def action_pause(self) -> None:
        pass

    def prot(self):

        wid_plt = self.query_one(PlotextPlot)
        plt = wid_plt.plt

        plt.ylabel("Páginas Processadas")

        try:
            down_count, url_count = self.engine_inst.rate_value()
            self.historico_down.append(down_count)
            self.historico_url.append(url_count)

            plt.clear_data()
            plt.clear_figure()
            plt.xticks(list(""))

            self.historico_x.append(len(self.historico_x) + 1)

            if len(self.historico_x) > 30:
                self.historico_x.pop(0)
                self.historico_down.pop(0)
                self.historico_url.pop(0)

            plt.plot(
                self.historico_x,
                self.historico_down,
                label="Downloads",
                color="green",
                style="void",
                marker="braille",
            )
            plt.plot(
                self.historico_x,
                self.historico_url,
                label="URLs",
                color="blue",
                style="void",
                marker="braille",
            )

            wid_plt.refresh()

        except Exception as e:
            pass

    @work(thread=True)
    def start_run(self):

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

        for key_dict, key_row in tipos.items():
            table = self.query_one("#down_table", DataTable)

            valor_concluido = message.concluida.get(key_dict, [])
            valor_pendente = message.pendente.get(key_dict, 0)
            valor_total = message.total.get(key_dict, 0)

            table.update_cell(key_row, "ok", str(valor_concluido))
            table.update_cell(key_row, "rest", str(valor_pendente))
            table.update_cell(key_row, "total", str(valor_total))

        table = self.query_one("#threads_table", DataTable)
        thread_infos = message.threads_info

        for info in thread_infos:
            id_thread = str(info["id"])
            name = str(info["name"])
            cat = str(info["Categoria"])
            status = str(info["status"])
            try:
                table.update_cell(name, "id_column", id_thread)
                table.update_cell(name, "name_column", name)
                table.update_cell(name, "cat_column", cat)
                table.update_cell(name, "status_column", status)

            except CellDoesNotExist:
                table.add_row(id_thread, name, cat, status, key=name)
