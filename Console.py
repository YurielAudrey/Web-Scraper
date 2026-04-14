import os
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
import pyfiglet
from rich import print
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
import ws

layout = Layout()
table_url = Table()

style_1= "White Bold"



class Console:
    def __init__(self,title,version):
        self.title = title
        self.version = version
        self.ua = {"User-Agent": "Python/3.14"}
        self.url_inicial = "https://pt.wikipedia.org//wiki/Wikip%C3%A9dia:P%C3%A1gina_principal"
        self.ws = ws.ws(self.url_inicial,self.ua)
        self.console("asd","1.1")
        #self.layout_test(title,version)



    #teste Apgar depois de implementar no lugar certo
    def layout_test(self,t,v):
        table_url.add_column("ID", justify="center", style=style_1,width = 10)
        table_url.add_column("URL", justify="center", style=style_1,width = 80)


        layout.split_column(
            Layout(name="Historico"),
            Layout(name="Lower")
        )
        layout["Lower"].split_row(
            Layout(name="info"),
            Layout(name="erros",)
        )
        layout["Historico"].split(
            Layout(table_url)
        )

        print(layout)




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
            code, page_url, img_url  = self.ws.start_new(self.url_inicial,self.ua)
        elif x == "2":
            code, page_url, img_url = self.ws.start_save(self.ua)
        elif x == "3":
            pass
        else:
            pass
