import os
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
import pyfiglet
from rich import print
from rich.layout import Layout
import func as f
from rich.live import Live
from rich.table import Table

layout = Layout()
table = Table()

class Console:
    def __init__(self,title,version):
        self.title = title
        self.version = version

        self.layout_test(title,version)




    def layout_test(self,t,v):
        layout.split_column(
            Layout(name="upper"),
            Layout(name="Lower")
        )
        layout["Lower"].split_row(
            Layout(name="Left"),
            Layout(name="right")
        )
        print(layout)
        with Live(table,refresh_per_second=4):




    def title_show(self,title,version):
        title = pyfiglet.figlet_format(f"{title}", font="roman")
        panel = Panel(
            Align.center(f"[bold green]{title}"),
            subtitle=f"[bold blue]V:{version} | By Yuriel Audrey[/bold blue]",
            border_style="bold white",
            padding=(1, 0)
        )
        print(panel)



    def console(self,t,v):
        ua = {"User-Agent": "Python/3.14"}
        self.title_show(t,v)
        print("Digite A opcao")
        print("1-Iniciar Novo")
        print("2-Continuar Anterior")
        print("3-Sair")
        x = Prompt.ask("Escolha a opcao: ",choices=["1","2","3"])
        os.system('cls')


        if x == "1":
            url_inicial = Prompt.ask("Digite a Url Inicial(deixe vazio para usar o wikipedia como padrao)")
            if url_inicial == "":
                url_inicial = "https://pt.wikipedia.org//wiki/Wikip%C3%A9dia:P%C3%A1gina_principal"


            code , html = f.get_html(url_inicial, ua)
            page_url, img_url = f.get_url(html)
            f.save_url(page_url)

        elif x == "2":
            pass
        elif x == "3":
            pass
        else:
            pass
