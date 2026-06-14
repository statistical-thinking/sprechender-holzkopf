# Sprechender Holzkopf
Ein Holzkopf auf Basis des Raspberry Pi Pico 1 / 2 und Raspberry Pi Pico 2W für Speech-to-Text und Text-to-Speech Anwendungen. Es wurde für ehrenamtliche Bildungsprojekte an allgemeinbildenden Schulen entwickelt, um Künstliche Intelligenz für Kinder und Jugendliche greifbar und verständlich zu machen. Das Ziel des Projekts ist nicht, einen fertigen Sprachassistenten für den Alltag bereitzustellen oder eine vollständig reproduzierbare Unterrichtslösung anzubieten. Vielmehr dient das System als Eisbrecher, um Interesse an Informatik, Statistik und Künstlicher Intelligenz zu wecken und Gespräche über Chancen und Grenzen moderner KI-Systeme anzuregen.

# Autor
Prof. Dr. habil. Dennis Klinkhammer

# Pädagogische Motivation
Viele Kinder kennen Künstliche Intelligenz lediglich als abstraktes Konzept oder aus kommerziellen Anwendungen. Dieses Projekt soll zeigen, dass KI-Systeme aus nachvollziehbaren technischen Komponenten bestehen und von Menschen entwickelt werden.

Der Raspberry Pi macht die Technik sichtbar und greifbar. Dadurch entstehen natürliche Gesprächsanlässe, beispielsweise:

Wie funktioniert Spracherkennung?
Was passiert mit den gesprochenen Fragen?
Können KI-Systeme Fehler machen?
Warum sollten Menschen die Ergebnisse von KI-Systemen kritisch hinterfragen?

Das Projekt versteht sich ausdrücklich als Demonstrator und Gesprächsanlass, nicht als Unterrichtsgegenstand oder fertige Unterrichtslösung.

# Benötigte Hardware
* 2 x Raspberry Pi Pico 1 / 2
* 1 x Raspberry Pi Zero 2W
* 1 x microSD-Karte mir Raspberry Pi OS
* 1 x Waveshare GPIO Expander For Raspberry Pi Pico (SKU 20477)
* 3 x Waveshare RGB Full-color LED Matrix Panel (SKU 20170)
* 1 x BerryBase USB Mini Mikrofon (EAN: 4251266751472)
* 1 x BerryBase externer USB Mini-Lautsprecher (EAN: 6945379550159)
* sowie entspr. Powerbank(s), USB-Kabel, Micro-USB-auf-USB-A-Adapter und USB-Presenter

Je nach verwendeter Audiohardware müssen die ALSA-Geräte angepasst werden.

# Softwarevoraussetzungen

Systempakete installieren:
```
sudo apt update
sudo apt install -y python3-pip python3-venv alsa-utils ffmpeg
```
Virtuelle Umgebung erstellen:

python3 -m venv .venv
source .venv/bin/activate

Benötigte Python-Pakete installieren:

pip install openai python-dotenv evdev

Zusätzlich werden folgende Programme verwendet:

arecord für die Audioaufnahme
aplay für die Audioausgabe
ffmpeg zur Umwandlung der erzeugten MP3-Dateien in WAV-Dateien
