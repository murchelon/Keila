from threading import Event
from core.state_manager import StateManager, state_type
from bib.uteis import log_term, sleep
import time

# Você precisa criar essas funções
from bib.audio_Record import recordAudio
from bib.audio_Playback import playAudio
from bib.api_AI import askAI
from bib.api_SpeachToText import speachToText
from bib.api_TextToSpeach import textToSpeach




def start_action_VoicePrompt(stop_event: Event, state_manager: StateManager) -> None:
    log_term("[ACTION] VoicePrompt - INIT")
    state_manager.set_state(state_type.RUNNING)

    inicio = time.monotonic()
    time_limit_toRun = 40  # seconds

    try:
        # 1. Gravar áudio
        log_term("[ACTION] VoicePrompt - RECORD AUDIO")
        audio_path = recordAudio(stop_event, time_limit_toRun)
        if stop_event.is_set():
            raise InterruptedError("Canceled during recording")

        # 2. Transcrever com speech-to-text
        log_term("[ACTION] VoicePrompt - TRANSCRIBE AUDIO")
        texto = speachToText(audio_path)
        if not texto:
            log_term("Nenhum texto reconhecido.")
            return

        if stop_event.is_set():
            raise InterruptedError("Canceled during Convert speach-to-text")

        # 3. Obter resposta do GPT
        log_term("[ACTION] VoicePrompt - SEND TEXT TO GPT")
        resposta = askAI(texto)

        if stop_event.is_set():
            raise InterruptedError("Canceled during Send to GPT")

        # 4. Converter para áudio com text-to-speech
        log_term("[ACTION] VoicePrompt - CONVERT TEXT TO AUDIO")
        resposta_audio_path = textToSpeach(resposta)

        if stop_event.is_set():
            raise InterruptedError("Canceled during Convert text-to-speach")

        # 5. Tocar resposta
        log_term("[ACTION] VoicePrompt - PLAYING ANSWER")
        playAudio(resposta_audio_path)

        if stop_event.is_set():
            raise InterruptedError("Canceled during playing audio")        

    except InterruptedError as e:
        log_term(f"[ACTION] VoicePrompt - CANCELED ({str(e)})")

    except Exception as e:
        log_term(f"[ACTION] ERROR during processing: {str(e)}")

    finally:
        log_term("[ACTION] VoicePrompt - END")
        state_manager.set_state(state_type.READY)
