import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from Actions.VoicePrompt.VoicePrompt import start_action_VoicePrompt
from ui.screen import init_ui
from state.state_manager import StateManager, state_type
from hardware.leds import init_leds
from common.types import ApiRetStatusCode, ApiRetStatus
from bib.uteis import log_term, sleep_async, sleep
from bib.threadManager import ThreadManager
from bib.config import KeilaConfig

keila_config = KeilaConfig.instance()

load_dotenv()

KEILA_VERSION = os.getenv("KEILA_VERSION")
KEILA_ENV = os.getenv("KEILA_ENV")


global_STATE = StateManager()

thread_manager = ThreadManager()

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("")
    log_term(f"=================", "BLUE")
    log_term(f"==  KEILA {KEILA_VERSION}  ==", "BLUE")
    log_term(f"=================", "BLUE")

    global_STATE.set_state(state_type.INIT)

    init_leds()
    init_ui()

    # threading.Thread(target=start_ui, args=(global_STATE,), daemon=True).start()
    global_STATE.set_state(state_type.READY)
    log_term("[MAIN] Keila is ready")
    log_term("Chave atual: " + str(keila_config.get("openai_api_key")))
    print("")

    yield
    log_term("[MAIN] Keila is shutting down")
    print("")


app = FastAPI(lifespan=lifespan)

@app.post("/api/actions/VoicePrompt")
async def action_VoicePrompt():
    log_term("[API] Route: /api/actions/VoicePrompt", "BLUE")

    if global_STATE.get_state() != state_type.READY.name:
        return {
            "prod": "KEILA",
            "version": KEILA_VERSION,
            "env": KEILA_ENV,
            "global_STATE": global_STATE.get_state(),
            "statusCode": ApiRetStatusCode.BUSY.name,
            "msg": "Please, wait ..."        
        }

    global_STATE.set_state(state_type.RUNNING)

    thread_manager.start_thread(
        "VoicePrompt",
        start_action_VoicePrompt,
        args=(global_STATE,)
    )
    

    return {
        "prod": "KEILA",
        "version": KEILA_VERSION,
        "env": KEILA_ENV,
        "global_STATE": global_STATE.get_state(),
        "statusCode": ApiRetStatusCode.OK.name,
        "msg": "Action: Starded"        
    }


@app.post("/api/cancelActions")
async def cancelActions():
    log_term("[API] Route: /api/cancelActions", "BLUE")

    global_STATE.set_state(state_type.CANCELING)

    # acoes para cancelar - mata o processo
    thread_manager.stop_all()


    retApiRetStatus = ApiRetStatus(ApiRetStatusCode.OK, "")

    global_STATE.set_state(state_type.READY)

    return {
        "prod": "KEILA",
        "version": KEILA_VERSION,
        "env": KEILA_ENV,
        "global_STATE": global_STATE.get_state(),
        "statusCode": retApiRetStatus.status_code.name,
        "msg": "Canceling all actions"        
    }



@app.get("/api/getInfo")
async def getInfo():
    log_term("[API] Route: /api/getInfo", "BLUE")
    retApiRetStatus = ApiRetStatus(ApiRetStatusCode.OK, "")

    return {
        "prod": "KEILA",
        "version": KEILA_VERSION,
        "env": KEILA_ENV,
        "global_STATE": global_STATE.get_state(),
        "statusCode": retApiRetStatus.status_code.name,
        "msg": "Info about Keila!"        
    }