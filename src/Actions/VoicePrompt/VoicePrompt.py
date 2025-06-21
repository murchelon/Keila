from bib.uteis import log_term, sleep
from core.state_manager import StateManager, state_type
import time

def start_action_VoicePrompt(stop_event, state_manager: StateManager):

    log_term("[ACTION] VoicePrompt - INIT")

    inicio = time.monotonic()
    tempo_limite = 40  # segundos



    while time.monotonic() - inicio < tempo_limite:
        # Faça o processamento

        if stop_event.is_set():
            log_term("[ACTION] VoicePrompt - CANCELADO")
            break

        sleep(0.1)

        pass
    # Finalize o que for necessário
    #     

    log_term("[ACTION] VoicePrompt - END")

    state_manager.set_state(state_type.READY)
    
    