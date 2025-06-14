
from core.state_manager import State

def process_flow(state, audio_data):
    from voice.speaker import speak
    from voice.listener import transcribe_audio
    from core.gpt_client import send_to_gpt

    if state.get_state() == State.RUNNING:
        state.set_state(State.LISTENING)
        text = transcribe_audio(audio_data)

        if state.get_state() == State.CANCELING:
            return

        state.set_state(State.RUNNING)  # await gpt
        response = send_to_gpt(text)

        if state.get_state() == State.CANCELING:
            return

        state.set_state(State.SPEAKING)
        speak(response)

        state.set_state(State.RUNNING)