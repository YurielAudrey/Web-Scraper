from textual.app import ComposeResult
from textual.layouts import vertical
from textual.screen import ModalScreen
from textual.containers import Grid, Vertical
from textual.widgets import Button, Label


class ErrorScreen(ModalScreen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    CSS_PATH = "../css/error_Screen.tcss"

    def compose(self) -> ComposeResult:

        with Vertical(classes="QuadradoModal"):
            yield Label(content=self.message, classes="LabelErro")
            yield Button(label="OK", id="ok", classes="ButtonErro")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "ok":
            self.dismiss()
