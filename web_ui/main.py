from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from tcp_client import TcpBankClient


app = FastAPI(title="P2P Bank Web UI")

app.mount("/static", StaticFiles(directory="web_ui/static"), name="static")
templates = Jinja2Templates(directory="web_ui/templates")

client = TcpBankClient()

state = {
    "host": client.cfg.host,
    "port": client.cfg.port,
    "timeout": client.cfg.timeout_s,
    "last_cmd": "",
    "last_response": "",
    "error": "",
}


def render(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "state": state,
        },
    )


def set_error(msg: str):
    state["error"] = msg


def clear_error():
    state["error"] = ""


def set_last(cmd: str, resp: str):
    state["last_cmd"] = cmd
    state["last_response"] = resp


def update_cfg_from_client():
    state["host"] = client.cfg.host
    state["port"] = client.cfg.port
    state["timeout"] = client.cfg.timeout_s


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return render(request)


@app.post("/connect", response_class=HTMLResponse)
def connect(
    request: Request,
    host: str = Form(...),
    port: int = Form(...),
    timeout: int = Form(2),
):
    clear_error()
    try:
        client.set_config(host=host.strip(), port=int(port), timeout_s=int(timeout))
        update_cfg_from_client()

        resp = client.send_cmd("BC")
        set_last("BC", resp)
    except Exception as e:
        set_error(f"Connect/Test failed: {e}")
    return render(request)


@app.post("/send", response_class=HTMLResponse)
def send_command(
    request: Request,
    cmd: str = Form(...),
):
    clear_error()
    cmd_clean = cmd.strip()
    state["last_cmd"] = cmd_clean
    try:
        resp = client.send_cmd(cmd)
        state["last_response"] = resp
    except Exception as e:
        set_error(str(e))
        state["last_response"] = ""
    return render(request)


@app.post("/cmd/bc", response_class=HTMLResponse)
def cmd_bc(request: Request):
    return send_command(request, cmd="BC")


@app.post("/cmd/ac", response_class=HTMLResponse)
def cmd_ac(request: Request):
    return send_command(request, cmd="AC")


@app.post("/cmd/ba", response_class=HTMLResponse)
def cmd_ba(request: Request):
    return send_command(request, cmd="BA")


@app.post("/cmd/bn", response_class=HTMLResponse)
def cmd_bn(request: Request):
    return send_command(request, cmd="BN")


@app.post("/cmd/ab", response_class=HTMLResponse)
def cmd_ab(
    request: Request,
    account_number: str = Form(...),
    bank_code: str = Form(...),
):
    cmd = f"AB {account_number.strip()}/{bank_code.strip()}"
    return send_command(request, cmd=cmd)


@app.post("/cmd/ad", response_class=HTMLResponse)
def cmd_ad(
    request: Request,
    account_number: str = Form(...),
    bank_code: str = Form(...),
    amount: str = Form(...),
):
    cmd = f"AD {account_number.strip()}/{bank_code.strip()} {amount.strip()}"
    return send_command(request, cmd=cmd)


@app.post("/cmd/aw", response_class=HTMLResponse)
def cmd_aw(
    request: Request,
    account_number: str = Form(...),
    bank_code: str = Form(...),
    amount: str = Form(...),
):
    cmd = f"AW {account_number.strip()}/{bank_code.strip()} {amount.strip()}"
    return send_command(request, cmd=cmd)


@app.post("/cmd/ar", response_class=HTMLResponse)
def cmd_ar(
    request: Request,
    account_number: str = Form(...),
    bank_code: str = Form(...),
):
    cmd = f"AR {account_number.strip()}/{bank_code.strip()}"
    return send_command(request, cmd=cmd)
