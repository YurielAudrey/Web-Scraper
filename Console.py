import os
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
import pyfiglet
from rich import print
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
import ws

style_1= "bold green"
layout = Layout()
table_url = Table()
table_info = Table()
table_resp = Table()


panel_hist = Panel.fit(table_url)
panel_info = Panel.fit(table_info)
panel_resp = Panel.fit(table_resp)


table_info.add_column("Desc", justify="center", style=style_1, width=10)
table_info.add_column("Valor", justify="center", style=style_1, width=10)
table_info.add_column("Total", justify="center", style=style_1, width=10)
table_info.add_column("%", justify="center", style=style_1, width=10)

table_resp.add_column("ID", justify="center", style=style_1, width=5)
table_resp.add_column("Code", justify="center", style=style_1, width=10)


table_url.add_column("ID", justify="center", style=style_1, width=5)
table_url.add_column("URL", justify="center", style=style_1, width=67)
table_url.add_column("Urls", justify="center", style=style_1, width=10)
table_url.add_column("Url_Img", justify="center", style=style_1, width=10)

layout.split_column(
    Layout(name="Historico"),
    Layout(name="Lower")
                )
layout["Lower"].split_row(
    Layout(name="info"),
    Layout(name="erros"),
    Layout(name="loading" )
                )

layout["Historico"].split(
    Layout(panel_hist)
)
layout["erros"].split(
    Layout(panel_resp)
)
layout["info"].split(
    Layout(panel_info)
)




class Console:
    def __init__(self,title,version):
        self.title = title
        self.version = version
        self.ua = {"User-Agent": "Python/3.14"}
        self.url_inicial = "https://pt.wikipedia.org//wiki/Wikip%C3%A9dia:P%C3%A1gina_principal"
        self.ws = ws.ws(self.url_inicial,self.ua)
        self.console("asd","1.1")
        #self.layout_test(title,version)

    #mostra o titlulo , tao inutil quanto parece
    def title_show(self,title,version):
        title = pyfiglet.figlet_format(f"{title}", font="roman")
        panel = Panel(
            Align.center(f"[bold green]{title}"),
            subtitle=f"[bold blue]V:{version} | By Yuriel Audrey[/bold blue]",
            border_style=style_1,
            padding=(1, 0)
        )
        print(panel)


    #Funcao principal do console , inutil mas nao dispensavel
    def console(self,t,v):

        self.title_show(t,v)
        print("Digite A opcao")
        print("1-Iniciar Novo")
        print("2-Continuar Anterior")
        print("3-Sair")
        x = Prompt.ask("Escolha a opcao: ",choices=["1","2","3"])
        os.system('cls')


        if x == "1":
            #self.ws.start_new(self.url_inicial,self.ua,table_url,panel)
            print(layout)
        elif x == "2":
            code, page_url, img_url = self.ws.start_save(self.ua)
        elif x == "3":
            pass
        else:
            pass
