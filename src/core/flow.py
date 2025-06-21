
from core.state_manager import state_type

def process_flow(state, audio_data):
    from voice.speaker import speak
    from voice.listener import transcribe_audio
    from core.gpt_client import send_to_gpt

    if state.get_state() == state_type.RUNNING:
        state.set_state(state_type.LISTENING)
        text = transcribe_audio(audio_data)

        if state.get_state() == state_type.CANCELING:
            return

        state.set_state(state_type.RUNNING)  # await gpt
        response = send_to_gpt(text)

        if state.get_state() == state_type.CANCELING:
            return

        state.set_state(state_type.SPEAKING)
        speak(response)

        state.set_state(state_type.RUNNING)