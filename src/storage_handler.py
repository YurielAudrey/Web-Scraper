import configparser
from pathlib import Path

encod = "utf-8"


# salva as url capturada para continuar posteriormente
def save_csv_url(urls: list, path: str, name: str):
    try:
        diretorio = Path(path) / "Horus"
        diretorio.mkdir(parents=True, exist_ok=True)
        path_full = diretorio / f"{name}.csv"

        with open(path_full, "w", encoding=encod) as f:
            fl = ""
            for url in urls:
                fl = f"{fl}\n,{url}"

            f.write(fl)

        return "[INFO] ARQUIVO SALVO"

    except Exception as e:

        return f"[WARN]{e}"


# le o arquivo com as url salva
def load_url(path: str, name: str):
    path = Path(path) / "Horus"
    path.mkdir(parents=True, exist_ok=True)
    path_full = path / f"{name}.csv"
    try:
        with open(path_full, "r", encoding=encod) as f:
            urls = f.readline().split(",")
            log = f"[INFO]Arquivo carregado"
            return log, urls
    except Exception as e:
        log = f"[ERROR]Exception:{e}"
        return log, []


# salva o arquivo na lista de download
def save_file(name_file: str, path, response):
    diretorio = path / "media"
    diretorio.mkdir(parents=True, exist_ok=True)
    path_full = diretorio / name_file
    with open(path_full, "wb") as f:
        f.write(response.content)

    return True


# cria o arquivo .ini
def save_cfg(**kwargs):
    config = configparser.ConfigParser()

    threads = kwargs["threads"]
    path = kwargs["path"]
    email = kwargs["email"]

    path_full = "config/config.ini"

    config["Geral"] = {
        "threads": threads,
        "path": path,
        "email": email,
    }

    config["Formatos"] = {
        "img": kwargs["img"],
        "videos": kwargs["videos"],
        "text": kwargs["text"],
        "all": kwargs["all"],
    }

    with open(path_full, "w") as configfile:
        config.write(configfile)


# transforma o arquivo .INI em um dict
def load_cfg() -> dict[str, int | str]:
    config = configparser.ConfigParser()
    path_full = "config/config.ini"

    config.read(path_full)
    try:
        threads = int(config["Geral"]["threads"])
        path = config["Geral"]["path"]
        email = config["Geral"]["email"]

        img_bool = config["Formatos"]["img"]
        video_bool = config["Formatos"]["videos"]
        text_bool = config["Formatos"]["text"]

        cfg = {
            "threads": threads,
            "path": path,
            "email": email,
            "img": img_bool,
            "video": video_bool,
            "text": text_bool,
        }

        return cfg

    except:
        cfg = {}
        return cfg
