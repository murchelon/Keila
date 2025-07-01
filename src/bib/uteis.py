from datetime import datetime
from colorama import init, Fore, Style
import asyncio
import time
import requests
from typing import Optional

def log_term(msg: str, color: str = "DEFAULT") -> None: 
    now = datetime.now()
    timestamp = now.strftime("[%d/%m/%Y %H:%M:%S]")

    if (color == "DEFAULT"):
        outColor = ""
    elif (color == "BLUE"):
        outColor = Fore.BLUE
    elif (color == "GREEN"):
        outColor = Fore.GREEN
    else:
        outColor = Fore.WHITE        

    print(f"{Fore.BLUE}K:{Style.RESET_ALL} {Fore.YELLOW}{timestamp}{Style.RESET_ALL}  {outColor}{msg}{Style.RESET_ALL}")


async def sleep_async(seconds: int) -> None:
    await asyncio.sleep(seconds)  

def sleep(seconds: float) -> None:
    time.sleep(seconds)  

def as_float(value, fallback: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback
    

def api_request(
    method: str,
    url: str,
    headers: Optional[dict] = None,
    body: Optional[dict] = None,
    use_json: bool = True,
    files: Optional[dict] = None,
    timeout: int = 30
):
    """
    Função padrão para requisições HTTP (GET, POST, PUT, DELETE, etc.)



    result = api_request(
        method="POST",
        url="https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        body={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}]
        },
        use_json=True
    )

    """
    try:
        log_term(f"[API_REQUEST] {method.upper()} para {url}")

        kwargs = {
            "method": method.upper(),
            "url": url,
            "headers": headers,
            "timeout": timeout
        }

        if files:
            kwargs["files"] = files
            kwargs["data"] = body  # arquivos + form-data
        else:
            if use_json:
                kwargs["json"] = body
            else:
                kwargs["data"] = body

        response = requests.request(**kwargs)
        response.raise_for_status()
        log_term(f"[API_REQUEST] Sucesso: {response.status_code}")
        return response.json()

    except requests.RequestException as e:
        log_term(f"[API_REQUEST] Erro: {e}")
        return None


def api_request_with_file(
    method: str,
    url: str,
    file_path: str,
    file_field_name: str = "file",
    headers: Optional[dict] = None,
    body: Optional[dict] = None,
    timeout: int = 30
):
    """
    Helper para requisições que enviam arquivos.
    Abre e fecha o arquivo automaticamente.

    result = api_request_with_file(
        method="POST",
        url="https://api.openai.com/v1/audio/transcriptions",
        file_path="temp/audio.wav",
        headers={"Authorization": f"Bearer {api_key}"},
        body={"model": "whisper-1"}
    )
        
    """
    try:
        with open(file_path, "rb") as f:
            files = {file_field_name: f}
            return api_request(
                method=method,
                url=url,
                headers=headers,
                body=body,
                use_json=False,  # quando tem arquivo, envia como form-data
                files=files,
                timeout=timeout
            )
    except IOError as e:
        log_term(f"[API_REQUEST_WITH_FILE] Erro ao abrir arquivo: {e}")
        return None



