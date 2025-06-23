
from bib.uteis import log_term, api_request_with_file


def SpeechToText(
    ai_who: str,
    ai_api_key: str,
    ai_endpoint: str,
    ai_model: str,
    audio_file: str
):
    """
    Função para enviar um arquivo de áudio à OpenAI e obter a transcrição usando Whisper.
    """
    log_term(f"[SpeechToText] START - {ai_who}")

    url = f"{ai_endpoint}"
    headers = {
        "Authorization": f"Bearer {ai_api_key}"
    }
    body = {
        "model": ai_model
    }

    result = api_request_with_file(
        method="POST",
        url=url,
        file_path=audio_file,
        headers=headers,
        body=body
    )

    if result is None:
        log_term(f"[SpeechToText] Falha na transcrição")
        return None

    text = result.get("text", "")
    log_term(f"[SpeechToText] FINISH - Transcrição: {text}")
    return text
