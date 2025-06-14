from bib.uteis import log_term

def send_to_gpt(text):
    log_term(f"[GPT] Enviando: {text}")
    return f"Resposta simulada para: {text}"