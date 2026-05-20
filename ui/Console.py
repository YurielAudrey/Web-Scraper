import os
import requests
from requests import Request

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Grid, Container
from textual.widgets import (
    Header,
    Footer,
    Rule,
    Label,
    Input,
    Button,
    Checkbox,
    SelectionList,
)

import core.storage_handler as sh
from ui.ErrorScreen import ErrorScreen
from ui.ProcessScreen import ProcessScreen


class Ui(App):

    TITLE = "Horus 1.0"
    CSS_PATH = "../css/layout.tcss"
    BINDINGS = [
        ("ctrl+s", "save_quit", "salvar e fechar"),
        ("ctrl+p", "pause", "pausar"),
    ]
    SCREENS = {
        "settings": ProcessScreen,
    }

    def compose(self) -> ComposeResult:
        yield Header(name="Horus", show_clock=True, classes="header")
        with Vertical(classes="run-container") as run:
            run.border_title = "Run"
            yield Vertical(
                self.preset_input(
                    texto_label="URL",
                    texto_input="https://www.google.com",
                    var_css="input_cfg var2",
                    id_name="url_input",
                    type_input="text",
                ),
                Horizontal(
                    Checkbox("Load", classes="Check", id="load_check"),
                    Checkbox("Isolar", classes="Check", id="isola_check"),
                    Button("RUN", classes="ButtonRun", id="run"),
                ),
            )

        with Vertical(classes="info-container") as info:
            info.border_title = "Infos"

        with Vertical(classes="config-container") as config:
            config.border_title = "config"
            yield self.preset_input(
                texto_label="email",
                texto_input="testando",
                var_css="a",
                id_name="email_input",
                type_input="text",
            )
            yield self.preset_input(
                texto_label="Path",
                texto_input="path",
                var_css="a",
                id_name="path_input",
                type_input="text",
            )

            yield self.preset_input(
                texto_label="Threads",
                texto_input="Threads",
                var_css="var1",
                id_name="threads_input",
                type_input="integer",
            )

            with Horizontal():
                yield SelectionList[bool](
                    ("Imagem", "img", False),
                    ("Video", "vid", False),
                    ("Texto", "txt", False),
                    ("Tudo", "all", False),
                    classes="listCheck",
                    id="types",
                )

                yield Button(
                    "Salvar Configuracao", classes="ButtonRun", id="config"
                )

        yield Footer(name="Footer")

    @staticmethod
    def preset_input(
        texto_label: str,
        texto_input: str,
        var_css: str,
        id_name: str,
        type_input,
    ) -> Horizontal:

        inp = Horizontal(
            Label(content=texto_label, classes="label_cfg"),
            Input(
                texto_input,
                classes=var_css,
                type=type_input,
                id=id_name,
            ),
            classes="horizontalInput",
        )
        return inp

    def on_mount(self):
        cfg = sh.load_cfg()
        t = cfg["threads"]

        self.query_one("#email_input", Input).value = cfg["email"]
        self.query_one("#threads_input", Input).value = str(t)
        self.query_one("#path_input", Input).value = cfg["path"]
        selection_list = self.query_one("#types", SelectionList)

        if cfg["img"] == "True":
            selection_list.select("img")
        if cfg["video"] == "True":
            selection_list.select("vid")
        if cfg["text"] == "True":
            selection_list.select("txt")

    # funcoes dos botoes da interface
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "config":
            email = self.query_one("#email_input", Input).value
            threads = self.query_one("#threads_input", Input).value
            path = self.query_one("#path_input", Input).value
            list_selection = self.query_one("#types", SelectionList)
            img = False
            vid = False
            txt = False
            all_opx = False
            if os.path.exists(path):
                for i in list_selection.selected:
                    if i == "img":
                        img = True
                    if i == "vid":
                        vid = True
                    if i == "txt":
                        txt = True
                    if i == "all":
                        all_opx = True

                sh.save_cfg(
                    threads=threads,
                    email=email,
                    path=path,
                    img=img,
                    videos=vid,
                    text=txt,
                    all=all_opx,
                )
            else:
                screen = ErrorScreen("Diretorio Inexistente")
                self.push_screen(screen)

        if event.button.id == "run":
            url = self.query_one("#url_input", Input).value
            isolation = self.query_one("#isola_check", Checkbox).value
            load = self.query_one("#load_check", Checkbox).value
            try:
                r = requests.get(url)
            except Exception as e:
                screen = ErrorScreen(f"{e}")
                self.push_screen(screen)
            else:
                cfg = sh.load_cfg()

                screen = ProcessScreen(url, cfg, isolation, load)
                self.push_screen(screen)
