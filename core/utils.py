from datetime import datetime


def fix_url(scheme, netloc, u):
    url = u
    if url.startswith("https://"):
        return url
    else:
        return f"{scheme}://{netloc}/{url}"


def log_Manager(msg: str):
    color = "white"
    if msg != "":
        timestamp = datetime.now().strftime("%H:%M:%S")
        if msg.startswith("[INFO]"):
            color = "green"
        elif msg.startswith("[DEBUG]"):
            color = "blue"
        elif msg.startswith("[WARN]"):
            color = "yellow"
        elif msg.startswith("[ERROR]"):
            color = "red"
        elif msg.startswith("[CRITICAL]"):
            color = "black on red"

        txt = f"[{color}]{timestamp} {msg} [/]"

        return txt
    return ""
