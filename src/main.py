from contextlib import asynccontextmanager
from fastapi import FastAPI
from hardware.leds import init_leds
from ui.tela import start_ui
from core.state_manager import StateManager, State
import threading

from dotenv import load_dotenv
import os

from bib.uteis import log_term, sleep_async, sleep
from common.types import ApiRetStatusCode, ApiRetStatus

load_dotenv()

KEILA_VERSION = os.getenv("KEILA_VERSION")
KEILA_ENV = os.getenv("KEILA_ENV")


global_STATE = StateManager()

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("")
    log_term(f"=================", "BLUE")
    log_term(f"==  KEILA {KEILA_VERSION}  ==", "BLUE")
    log_term(f"=================", "BLUE")

    global_STATE.set_state(State.INIT)
    init_leds()

    threading.Thread(target=start_ui, args=(global_STATE,), daemon=True).start()
    global_STATE.set_state(State.READY)
    log_term("[Main] Keila is ready")
    print("")

    yield
    log_term("[Main] Keila is shutting down")
    print("")


app = FastAPI(lifespan=lifespan)

@app.post("/api/initFlow_voice_prompt")
async def initFlow_voice_prompt():
    log_term("[API] Rota: /api/initFlow_voice_prompt", "BLUE")

    if global_STATE.get_state() != State.READY.name:
        return {
            "prod": "KEILA",
            "version": KEILA_VERSION,
            "env": KEILA_ENV,
            "global_STATE": global_STATE.get_state(),
            "statusCode": ApiRetStatusCode.BUSY.name,
            "msg": "Por favor, aguarde ..."        
        }

    log_term("[API] INIT initFlow_voice_prompt")

    global_STATE.set_state(State.LISTENING)

    await sleep_async(10)

    global_STATE.set_state(State.READY)

    log_term("[API] FINISH initFlow_voice_prompt")

    return {
        "prod": "KEILA",
        "version": KEILA_VERSION,
        "env": KEILA_ENV,
        "global_STATE": global_STATE.get_state(),
        "statusCode": ApiRetStatusCode.OK.name,
        "msg": "initFlow_voice_prompt finalizado"        
    }


@app.post("/api/cancel")
async def cancel():
    log_term("[API] Rota: /api/cancel", "BLUE")

    global_STATE.set_state(State.CANCELING)

    # acoes para cancelar

    global_STATE.set_state(State.READY)

    retApiRetStatus = ApiRetStatus(ApiRetStatusCode.OK, "")

    return {
        "prod": "KEILA",
        "version": KEILA_VERSION,
        "env": KEILA_ENV,
        "global_STATE": global_STATE.get_state(),
        "statusCode": retApiRetStatus.status_code.name,
        "msg": "All actions canceled"        
    }



@app.get("/api/getInfo")
async def get_getinfo():
    log_term("[API] Rota: /api/getInfo", "BLUE")
    retApiRetStatus = ApiRetStatus(ApiRetStatusCode.OK, "")

    return {
        "prod": "KEILA",
        "version": KEILA_VERSION,
        "env": KEILA_ENV,
        "global_STATE": global_STATE.get_state(),
        "statusCode": retApiRetStatus.status_code.name,
        "msg": "Info about Keila!"        
    }