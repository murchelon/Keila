from bib.uteis import log_term, sleep
from threading import Event

def recordAudio(stop_event: Event, time_limit_toRun: int):
    log_term("[AUDIO_RECORD] recordAudio - START")
    sleep(3)
    log_term("[AUDIO_RECORD] recordAudio - FINISH")

    return "path para o file"