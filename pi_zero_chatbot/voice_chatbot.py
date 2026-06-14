import socket
import subprocess
import time
from pathlib import Path

from dotenv import load_dotenv
from evdev import InputDevice, categorize, ecodes, list_devices
from openai import OpenAI


PROJECT_DIR = Path(__file__).parent

AUDIO_INPUT = PROJECT_DIR / "input.wav"
AUDIO_OUTPUT_MP3 = PROJECT_DIR / "answer.mp3"
AUDIO_OUTPUT_WAV = PROJECT_DIR / "answer.wav"
BEEP_FILE = PROJECT_DIR / "r2d2_beep.wav"

RECORDING_DEVICE = "plughw:0,0"
PLAYBACK_DEVICE = "plughw:1,0"

RECORD_SECONDS = 5

VALID_KEYS = {
    "KEY_PAGEDOWN",
    "KEY_RIGHT",
    "KEY_ENTER",
    "KEY_SPACE",
}


def wait_for_internet():
    while True:
        try:
            socket.create_connection(("api.openai.com", 443), timeout=5)
            print("Internet verfügbar")
            return
        except OSError:
            print("Warte auf Netzwerk...")
            time.sleep(10)


def find_presenter():
    print("Suche Presenter/Input-Gerät...")

    devices = [InputDevice(path) for path in list_devices()]

    for device in devices:
        print(f"Gefunden: {device.path} - {device.name}")

    for device in devices:
        name = device.name.lower()

        if (
            "presenter" in name
            or "keyboard" in name
            or "usb" in name
            or "receiver" in name
        ):
            print(f"Nutze Input-Gerät: {device.path} - {device.name}")
            return device

    raise RuntimeError("Kein passendes Presenter/Input-Gerät gefunden.")


def wait_for_presenter(device):
    print("\n➡️ Presenter-Taste drücken...")

    for event in device.read_loop():
        if event.type != ecodes.EV_KEY:
            continue

        key_event = categorize(event)

        if key_event.keystate != key_event.key_down:
            continue

        print(f"Taste erkannt: {key_event.keycode}")

        if key_event.keycode in VALID_KEYS:
            return


def beep():
    if not BEEP_FILE.exists():
        print(f"Piepton-Datei nicht gefunden: {BEEP_FILE}")
        return

    subprocess.run([
        "aplay",
        "-D", PLAYBACK_DEVICE,
        str(BEEP_FILE)
    ], check=False)


def record_audio(seconds: int = 5):
    print(f"🎙️ Aufnahme startet für {seconds} Sekunden...")

    for i in range(3):  # Retry-Mechanismus
        try:
            subprocess.run([
                "arecord",
                "-D", RECORDING_DEVICE,
                "-f", "cd",
                "-t", "wav",
                "-d", str(seconds),
                "-c", "1",
                "-r", "16000",
                str(AUDIO_INPUT)
            ], check=True)

            print("✅ Aufnahme beendet.")
            return

        except subprocess.CalledProcessError:
            print(f"⚠️ Audio busy – Retry {i+1}/3")
            time.sleep(0.5)

    raise RuntimeError("Mikrofon dauerhaft blockiert")


def transcribe_audio() -> str:
    print("📝 Transkribiere Sprache...")

    with AUDIO_INPUT.open("rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
            language="de"
        )

    return transcript.text.strip()


def ask_chatgpt(user_text: str) -> str:
    print("🤖 Erzeuge Antwort...")

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "Du bist ein freundlicher Sprachassistent für ein Schulprojekt. "
            "Antworte kurz, verständlich und kindgerecht. "
            "Vermeide lange Erklärungen."
        ),
        input=user_text
    )

    return response.output_text.strip()


def speak_text(text: str):
    print("🔊 Erzeuge Sprachausgabe...")

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Sprich freundlich, klar und gut verständlich auf Deutsch."
    ) as response:
        response.stream_to_file(AUDIO_OUTPUT_MP3)

    print("🔄 Wandle MP3 in WAV um...")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-loglevel", "error",
        "-i", str(AUDIO_OUTPUT_MP3),
        str(AUDIO_OUTPUT_WAV)
    ], check=True)

    print("🔊 Spiele Antwort über ALSA ab...")

    subprocess.run([
        "aplay",
        "-D", PLAYBACK_DEVICE,
        str(AUDIO_OUTPUT_WAV)
    ], check=True)


def main():
    print("Raspberry Pi Voice Chatbot")

    load_dotenv(PROJECT_DIR / ".env")
    wait_for_internet()

    global client
    client = OpenAI()

    presenter = find_presenter()

    while True:
        try:
            wait_for_presenter(presenter)

            beep()

            record_audio()

            user_text = transcribe_audio()
            print(f"👤 Du hast gesagt: {user_text}")

            if not user_text:
                print("Keine Sprache erkannt.")
                continue

            answer = ask_chatgpt(user_text)
            print(f"🤖 Antwort: {answer}")

            speak_text(answer)

        except OSError as error:
            print(f"Input-Gerät verloren oder Audiofehler: {error}")
            time.sleep(5)
            presenter = find_presenter()

        except Exception as error:
            print(f"Fehler: {error}")
            time.sleep(5)


if __name__ == "__main__":
    main()
