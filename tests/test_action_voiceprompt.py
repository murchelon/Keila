import sys
import types

from state.state_manager import StateManager


def test_start_action_voiceprompt(monkeypatch):
    if 'pyaudio' not in sys.modules:
        dummy = types.ModuleType('pyaudio')
        dummy.paInt16 = 8
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
        dummy.PyAudio = PyAudio
        sys.modules['pyaudio'] = dummy

    from Actions.VoicePrompt.VoicePrompt import start_action_VoicePrompt

    monkeypatch.setattr('Actions.VoicePrompt.VoicePrompt.record_audio_untill_silence',
                        lambda *args, **kwargs: 'tmp.wav')
    monkeypatch.setattr('Actions.VoicePrompt.VoicePrompt.SpeechToText',
                        lambda *args, **kwargs: 'hello')

    sm = StateManager()
    dummy_event = type('E', (), {'is_set': lambda self: False})()
    start_action_VoicePrompt(dummy_event, sm)
    assert sm.get_state() == 'READY'
