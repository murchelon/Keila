from threading import Event
from state.state_manager import StateManager, state_type
from bib.uteis import log_term, as_float
import time

# Você precisa criar essas funções
from audio.audio_Record import record_audio_untill_silence
from audio.audio_Playback import playAudio
from bib.api_AI import askAI
from AI.api_SpeechToText import SpeechToText
from bib.api_TextToSpeech import textToSpeech


from bib.config import KeilaConfig

from bib.threadManager import ThreadManager



keila_config = KeilaConfig.instance()


thread_manager_VoicePrompt = ThreadManager()


def start_action_VoicePrompt(stop_event: Event, state_manager: StateManager) -> None:
    log_term("[ACTION] VoicePrompt - INIT")
    state_manager.set_state(state_type.RUNNING)

    inicio = time.monotonic()
    time_limit_toRun = 60  # seconds
    record_filename = "./temp/VoicePrompt_record.wav"

    stillOK = True

    silence_threshold: float = as_float(keila_config.get("audio_record", "silence_threshold"), 320.0)
    silence_duration: float = as_float(keila_config.get("audio_record", "silence_duration"), 1.7)
    
    ai_who: str = str(keila_config.get("speechToText", "ai_who"))
    ai_api_key: str = str(keila_config.get("speechToText", "ai_api_key"))
    ai_endpoint: str = str(keila_config.get("speechToText", "ai_endpoint"))
    ai_model: str = str(keila_config.get("speechToText", "ai_model"))


    log_term("silence_threshold = " + str(silence_threshold))
    log_term("silence_duration = " + str(silence_duration))
    log_term("ai_who = " + ai_who)
    log_term("ai_api_key = " + ai_api_key)
    log_term("ai_endpoint = " + ai_endpoint)
    log_term("ai_model = " + ai_model)


    try:
        # 1. Gravar áudio
        log_term("[ACTION] VoicePrompt - RECORD AUDIO")
        audio_path = record_audio_untill_silence(stop_event, record_filename, silence_threshold, silence_duration, time_limit_toRun)
        if (stop_event.is_set()):
            raise InterruptedError("Canceled during recording")

        log_term("audio_path = " + audio_path)

        if (audio_path == ""):
            stillOK = False

        # # 2. Transcrever com speech-to-text
        if (stillOK):
            log_term("[ACTION] VoicePrompt - TRANSCRIBE AUDIO")

            texto = SpeechToText(ai_who, ai_api_key, ai_endpoint, ai_model, audio_path)
            if not texto:
                log_term("Nenhum texto reconhecido.")
                return


        state_manager.set_state(state_type.READY)

        # if stop_event.is_set():
        #     raise InterruptedError("Canceled during Convert Speech-to-text")

        # # 3. Obter resposta do GPT
        # log_term("[ACTION] VoicePrompt - SEND TEXT TO GPT")
        # resposta = askAI(texto)

        # if stop_event.is_set():
        #     raise InterruptedError("Canceled during Send to GPT")

        # # 4. Converter para áudio com text-to-speech
        # log_term("[ACTION] VoicePrompt - CONVERT TEXT TO AUDIO")
        # resposta_audio_path = textToSpeech(resposta)

        # if stop_event.is_set():
        #     raise InterruptedError("Canceled during Convert text-to-Speech")

        # # 5. Tocar resposta
        # log_term("[ACTION] VoicePrompt - PLAYING ANSWER")
        # playAudio(resposta_audio_path)

        # if stop_event.is_set():
        #     raise InterruptedError("Canceled during playing audio")        

    except InterruptedError as e:
        log_term(f"[ACTION] VoicePrompt - CANCELED ({str(e)})")

    except Exception as e:
        log_term(f"[ACTION] ERROR during processing: {str(e)}")

    finally:
        log_term("[ACTION] VoicePrompt - END")
        # state_manager.set_state(state_type.READY)
