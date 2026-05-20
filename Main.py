from ui import Console as c

title = "Horus"
version = "1.0"

""" annotacoes

falta criar :

-adcionar verificacao do arquivo old *prioridade 2
-mudar para baixar qualquer tipo de arquivo e nao so imagen *prioridade 2
-verificar como que salva texto para uso em ia  *prioridade 

criado sistema de
isolamento
delay
cfg
interface do console
threads
delay automatico em casos de 429



"""


def main():

    app = c.Ui()
    app.run()


if __name__ == "__main__":
    main()
