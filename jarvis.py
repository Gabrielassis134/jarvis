import pyaudio
import numpy as np
import time
import subprocess
import pyautogui

# Config
THRESHOLD = 100         # Sensibilidade 
CLAP_COOLDOWN = 0.4     # Tempo mínimo entre palmas (segundos)
WINDOW = 1.5            # Window de tempo para contar palmas
CHUNK = 1024            # Tamanho do bloco de áudio
RATE = 44100            # Taxa de amostragem

# oq esse butão faz??
def acao_1_palma():
    print("👏 1 palma detectada!")
    # para e volta
    pyautogui.press('playpause')

def acao_2_palmas():
    print("👏👏 2 palmas detectadas!")
    # abre algo
    subprocess.Popen("notepad.exe")

def acao_3_palmas():
    print("👏👏👏 3 palmas detectadas!")
    # desliga essa tela
    subprocess.Popen("rundll32.exe user32.dll,LockWorkStation")

# Detergente
def detectar_palmas():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("🎙️ Jarvis ativo! Ouvindo palmas...")
    print("   1 palma  → Abre CMD")
    print("   2 palmas → Abre Spotify + Google + VS Code")
    print("   3 palmas → Bloqueia a tela")
    print("   Ctrl+C para sair\n")

    palmas = []
    frames_alto = 0  # Conta por quanto time the som is alto

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio = np.frombuffer(data, dtype=np.int16)
            volume = np.max(np.abs(audio))
            agora = time.time()

            if volume > THRESHOLD:
                frames_alto += 1
            else:
                # som alto finish — verifyca if foi short ou long
                if frames_alto > 0:
                    if frames_alto <= 4:  # Palm = pico short 
                        palmas = [t for t in palmas if agora - t < WINDOW]
                        palmas.append(agora)
                        print(f"  👏 Palma! (volume: {volume}, duração: {frames_alto} frames) | Total: {len(palmas)}")
                    else:
                        print(f"  🗣️ Voz ignorada (duração: {frames_alto} frames)")
                    frames_alto = 0

            # Verifyca if passou a window sem new palm
            if palmas and (agora - palmas[-1]) > WINDOW:
                quantidade = len(palmas)
                palmas = []

                if quantidade == 1:
                    acao_1_palma()
                elif quantidade == 2:
                    acao_2_palmas()
                elif quantidade >= 3:
                    acao_3_palmas()

    except KeyboardInterrupt:
        print("\n👋 Jarvis desligado.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    detectar_palmas()