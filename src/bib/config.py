import os
import json

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'keila_config.json'))


# from bib.config import KeilaConfig

# cfg = KeilaConfig.instance()

# # Acesso
# print(cfg.get("audio", "silence_threshold", default=300))

# # Alteração via UI ou outro processo
# cfg.set("audio", "silence_threshold", value=280)
# cfg.save()

# # Em outro ponto: alguém salvou o JSON no disco?
# cfg.reload()  # Atualiza os dados em tempo real


class KeilaConfig:
    _instance = None

    def __init__(self):
        self._data = {}
        self._path = CONFIG_PATH
        self.load()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load(self):
        """Carrega o JSON do disco (usado no init)"""
        if os.path.exists(self._path):
            with open(self._path, 'r') as f:
                self._data = json.load(f)
        else:
            self._data = {}

    def reload(self):
        """Força recarregamento do arquivo JSON atual"""
        self.load()

    def save(self):
        """Salva o JSON atual para o disco"""
        with open(self._path, 'w') as f:
            json.dump(self._data, f, indent=4)

    def get(self, *path, default=None):
        """Acessa um valor aninhado com segurança"""
        value = self._data
        for key in path:
            if not isinstance(value, dict):
                return default
            value = value.get(key)
            if value is None:
                return default
        return value

    def set(self, *path, value):
        """Exemplo: set("audio", "silence_threshold", value=300)"""
        d = self._data
        for key in path[:-1]:
            d = d.setdefault(key, {})
        d[path[-1]] = value

    def data(self):
        """Retorna o dicionário inteiro"""
        return self._data

    def path(self):
        """Retorna o caminho do arquivo de configuração"""
        return self._path
