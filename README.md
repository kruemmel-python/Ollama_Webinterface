
# Ollama Gradio App mit Datei-Upload

![image](https://github.com/user-attachments/assets/6a11b726-6be1-4b27-8f92-6b1e65fef1a7)


## Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Funktionen](#funktionen)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
  - [1. Python und Pip installieren](#1-python-und-pip-installieren)
  - [2. Projektklon und Abhängigkeiten installieren](#2-projektklon-und-abhängigkeiten-installieren)
  - [3. Ollama installieren](#3-ollama-installieren)
  - [4. Modelle hinzufügen](#4-modelle-hinzufügen)
- [Verwendung](#verwendung)
- [Projekstruktur](#projekstruktur)
- [Beitrag leisten](#beitrag-leisten)
- [Lizenz](#lizenz)
- [Kontakt](#kontakt)

## Über das Projekt

Die **Ollama Gradio App mit Datei-Upload** ist eine benutzerfreundliche Webanwendung, die es ermöglicht, Text-
und PDF-Dateien hochzuladen, deren Inhalt zu analysieren und intelligente Antworten von Ollama-Modellen zu
generieren. Die App nutzt [Gradio](https://gradio.app/) für die Benutzeroberfläche und
 [Ollama](https://ollama.com/) zur Textgenerierung.

### Hauptmerkmale

- **Datei-Upload:** Unterstützt das Hochladen von TXT- und PDF-Dateien zur Analyse.
- **Live-Antworten:** Generiert Antworten in Echtzeit, während das Modell die Eingabe verarbeitet.
- **Modellauswahl:** Wähle aus einer Vielzahl von vorinstallierten Ollama-Modellen.
- **Statusanzeigen:** Informiert den Benutzer über den aktuellen Status der Anfrage.

## Funktionen

- **Text- und PDF-Verarbeitung:** Extrahiert Text aus hochgeladenen Dateien und verarbeitet ihn.
- **ANSI-Code-Bereinigung:** Entfernt unerwünschte Steuerzeichen und spezielle Escape-Sequenzen aus der Ausgabe.
- **Live-Generierung:** Zeigt die generierte Antwort Schritt für Schritt an.
- **Benutzerfreundliche Oberfläche:** Einfache Bedienung durch klare Eingabe- und Ausgabefelder.

## Voraussetzungen

Bevor du mit der Installation beginnst, stelle sicher, dass du die folgenden Voraussetzungen erfüllst:

- **Betriebssystem:** Windows, macOS oder Linux
- **Python:** Version 3.7 oder höher
- **Ollama:** Installiert und konfiguriert

## Installation

### 1. Python und Pip installieren

Stelle sicher, dass Python 3.7 oder höher auf deinem System installiert ist. Du kannst die Installation überprüfen, indem du folgende Befehle im Terminal ausführst:

```bash
python --version
pip --version
```

Falls Python nicht installiert ist, lade es von der [offiziellen Webseite](https://www.python.org/downloads/) herunter und installiere es.

### 2. Projekt klonen und Abhängigkeiten installieren

Clone das Repository und installiere die notwendigen Python-Pakete:

```bash
# Repository klonen
git clone https://github.com/kruemmel-python/Ollama_Webinterface.git

# In das Projektverzeichnis wechseln
cd Ollama-Gradio-App

# Abhängigkeiten installieren
pip install -r requirements.txt
```

**Hinweis:** Stelle sicher, dass du dich im richtigen Verzeichnis befindest und dass `requirements.txt` alle benötigten Pakete enthält:

```txt
subprocess
re
gradio
time
PyPDF2
```

### 3. Ollama installieren

Ollama ist ein essentielles Werkzeug für diese Anwendung. Folge den Schritten unten, um Ollama auf deinem System zu installieren:

1. **Ollama herunterladen:**
   Besuche die [offizielle Ollama-Website](https://ollama.com/) und lade das passende Installationspaket für dein Betriebssystem herunter.

2. **Installation ausführen:**
   Führe das Installationspaket aus und folge den Anweisungen auf dem Bildschirm.

3. **Installation überprüfen:**
   Nach der Installation kannst du die erfolgreiche Installation überprüfen, indem du im Terminal folgenden Befehl ausführst:

   ```bash
   ollama --version
   ```

   Dies sollte die installierte Version von Ollama anzeigen.

### 4. Modelle hinzufügen

Um die Anwendung nutzen zu können, müssen die gewünschten Ollama-Modelle installiert und in den Code integriert werden. Folge diesen Schritten:

1. **Modelle installieren:**
   Verwende den Ollama-Befehl, um Modelle zu installieren. Beispiel:

   ```bash
   ollama install phi4:latest
   ollama install wizardlm2:7b-fp16
   # Füge weitere Modelle nach Bedarf hinzu
   ```

2. **Modelle im Code hinzufügen:**
   Öffne die `main.py` (oder wie auch immer deine Hauptdatei heißt) und finde die Liste der Modelle:

   ```python
   MODELS = [
       "phi4-model:latest",
       "phi4:latest",
       "wizardlm2:7b-fp16",
       "unzensiert:latest",
       "llama2-uncensored:7b-chat-q8_0",
       "teufel:latest",
       "Odin:latest",
       "luzifer:latest",
       "llama3:latest",
       "llama2-uncensored:latest"
   ]
   ```

   - **Hinzufügen neuer Modelle:** Füge die Namen der installierten Modelle als Strings in die `MODELS`-Liste ein. Zum Beispiel:

     ```python
     MODELS = [
         "phi4-model:latest",
         "phi4:latest",
         "wizardlm2:7b-fp16",
         "dein-neues-modell:version",
         # Weitere Modelle...
     ]
     ```

   - **Standardmodell festlegen:** Das Standardmodell wird durch die Konstante `DEFAULT_MODEL` festgelegt. Ändere dies nach Bedarf:

     ```python
     DEFAULT_MODEL = "phi4:latest"  # Ändere dies zu deinem bevorzugten Modell
     ```

## Verwendung

Nachdem du alle Schritte zur Installation abgeschlossen hast, kannst du die Anwendung starten und verwenden:

1. **Starten der Anwendung:**

   ```bash
   python main.py
   ```

   **Hinweis:** Stelle sicher, dass du im Projektverzeichnis bist.

2. **Zugriff auf die Weboberfläche:**
   Nach dem Start öffnet sich eine URL (z.B., `http://127.0.0.1:7860/`) in deinem Browser. Wenn du `share=True` in der `interface.launch()`-Funktion festgelegt hast, erhältst du auch einen öffentlichen Link.

3. **Verwendung der App:**
   - **Text eingeben:** Gib deine Frage oder deinen Text in das Textfeld ein.
   - **Modell auswählen:** Wähle das gewünschte Modell aus dem Dropdown-Menü.
   - **Datei hochladen (optional):** Lade eine TXT- oder PDF-Datei hoch, um deren Inhalt zu analysieren.
   - **Antwort anzeigen:** Die generierte Antwort wird in Echtzeit angezeigt.

## Projektstruktur

```
Ollama-Gradio-App/
├── main.py                # Hauptanwendungsskript
├── requirements.txt       # Python-Abhängigkeiten
├── README.md              # Projektbeschreibung
├── banner.png             # Bannerbild (optional)
└── weitere_dateien/...    # Zusätzliche Dateien und Ordner
```

## Beitrag leisten

Beiträge zur Verbesserung dieses Projekts sind willkommen! Folge diesen Schritten, um beizutragen:

1. **Fork das Repository**
2. **Erstelle einen neuen Branch:**

   ```bash
   git checkout -b feature/NeuesFeature
   ```

3. **Commit deine Änderungen:**

   ```bash
   git commit -m "Füge neues Feature hinzu"
   ```

4. **Push zum Branch:**

   ```bash
   git push origin feature/NeuesFeature
   ```

5. **Öffne einen Pull Request**

## Lizenz

Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert. Weitere Informationen findest du in der LICENSE-Datei.


---

*Dieses Projekt wurde mit ❤️ entwickelt.*

```
