import pyaudio
import numpy as np

CHUNK = 1024
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("🎙️ Calibrador ativo! Veja os volumes abaixo:")
print("   → Fique em silêncio e veja o volume do ambiente")
print("   → Fale normalmente e veja o volume da voz")
print("   → Bata palma e veja o volume da palma")
print("   Ctrl+C para sair\n")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio = np.frombuffer(data, dtype=np.int16)
        volume = np.max(np.abs(audio))

        if volume < 500:
            label = "😶 Silêncio"
        elif volume < 2000:
            label = "🔈 Som baixo"
        elif volume < 5000:
            label = "🗣️ Voz / Som médio"
        elif volume < 10000:
            label = "🔊 Som alto"
        else:
            label = "💥 Muito alto (palma?)"

        barra = "█" * (volume // 1000)
        print(f"  Volume: {volume:6} | {barra:30} | {label}")

except KeyboardInterrupt:
    print("\n✅ Calibração encerrada.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()