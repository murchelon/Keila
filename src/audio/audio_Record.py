import os
from threading import Event
import numpy as np
import pyaudio
import wave

from bib.uteis import log_term, sleep




def record_audio_untill_silence(stop_event: Event, 
                                output_filename: str = './temp/audio.wav', 
                                silence_threshold: float = 320,  
                                silence_duration: float = 1.7, 
                                max_duration: float = 60) -> str:
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print("[KEILA] Gravando...")
    frames = []
    silent_chunks = 0
    silence_limit = int(RATE / CHUNK * silence_duration)
    max_chunks = int(RATE / CHUNK * max_duration)

    for i in range(max_chunks):
        if stop_event.is_set():
            print("[KEILA] Gravação cancelada.")
            break

        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

        # Convertendo os bytes para int16
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()  # Volume médio (magnitude)


        print(f"[{i}] Volume médio: {volume:.2f} | Silent Chunks: {silent_chunks}/{silence_limit}")

        if volume < silence_threshold:
            silent_chunks += 1
        else:
            silent_chunks = 0

        if silent_chunks > silence_limit:
            print("[KEILA] Silêncio detectado. Parando gravação.")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("[KEILA] Áudio salvo:", output_filename)
    return output_filename
