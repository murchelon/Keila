from enum import Enum

class ApiRetStatusCode(Enum):
    ERROR = 0
    OK = 1
    BUSY = 2

class ApiRetStatus:
    def __init__(self, status_code: ApiRetStatusCode, status_msg: str):
        self.status_code = status_code
        self.status_msg = status_msg

# # Criando o objeto
# resposta = ApiRetStatus(ApiRetStatusCode.OK)

# print(resposta.status_code)         # ApiRetStatusCode.OK
# print(resposta.status_code.name)    # OK
# print(resposta.status_code.value)   # 1
