import os
import sys
import json
import shutil
import types
import pytest
import pathlib

base_dir = pathlib.Path(__file__).resolve().parent.parent
src_dir = base_dir / 'src'
sys.path.insert(0, str(src_dir))

if 'pyaudio' not in sys.modules:
    dummy = types.ModuleType('pyaudio')
    dummy.paInt16 = 8 # type: ignore

    class PyAudio:
        def open(self, *args, **kwargs):
            class Stream:
                def read(self, *a, **kw):
                    return b''
                def stop_stream(self):
                    pass
                def close(self):
                    pass
            return Stream()

        def get_sample_size(self, *args):
            return 2

        def terminate(self):
            pass

    dummy.PyAudio = PyAudio # type: ignore
    sys.modules['pyaudio'] = dummy



@pytest.fixture(scope="session", autouse=True)
def prepare_config():
    """Create keila_config.json from example for tests."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    src_dir = os.path.join(base_dir, 'src')
    example = os.path.join(src_dir, 'keila_config.example.json')
    config = os.path.join(src_dir, 'keila_config.json')
    shutil.copy(example, config)
    os.environ.setdefault('KEILA_VERSION', 'test')
    os.environ.setdefault('KEILA_ENV', 'test')
    yield
    if os.path.exists(config):
        os.remove(config)


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    import main
    return TestClient(main.app)
