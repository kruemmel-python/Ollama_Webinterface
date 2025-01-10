import subprocess  # Zum Ausführen von externen Prozessen
import re  # Für reguläre Ausdrücke zur Textverarbeitung
import gradio as gr  # Für die Erstellung der Benutzeroberfläche
import time  # Für zeitbezogene Funktionen
from PyPDF2 import PdfReader  # Zum Lesen von PDF-Dateien

# =============================================================================
# Konstanten
# =============================================================================

# Reguläre Ausdrücke zur Bereinigung der Ausgaben
ANSI_ESCAPE_REGEX = re.compile(r'(?:\x1B[@-_]|[\x1B\x9B][0-?]*[ -/]*[@-~])')
OLLAMA_ESCAPE_REGEX = re.compile(r'\?\d+[lh]')
LOADING_CHARS_REGEX = re.compile(r'[\u2800-\u28FF]')
CARRIAGE_RETURN_REGEX = re.compile(r'\r')
CUSTOM_TEXT_REGEX = re.compile(r'2K1G ?(?:2K1G)*!?')

# Liste der verfügbaren Modelle
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

# Standardmodell, das verwendet wird, wenn kein anderes ausgewählt wird
DEFAULT_MODEL = "phi4:latest"

# Statusnachrichten, die dem Benutzer angezeigt werden
STATUS_MESSAGE_GENERATING = "Antwort wird generiert..."
STATUS_MESSAGE_COMPLETE = "Antwort generiert."
STATUS_MESSAGE_ERROR = "Fehler: Die Anfrage konnte nicht verarbeitet werden."

# =============================================================================
# Funktionen zur Verarbeitung und Bereinigung der Ausgaben
# =============================================================================

def clean_output(output: str) -> str:
    """
    Entfernt unerwünschte Steuerzeichen und spezifische Escape-Sequenzen aus dem Output.

    Args:
        output (str): Der ursprüngliche Textoutput.

    Returns:
        str: Der bereinigte Textoutput.
    """
    cleaned_output = ANSI_ESCAPE_REGEX.sub('', output)  # Entfernt ANSI-Steuercodes
    cleaned_output = OLLAMA_ESCAPE_REGEX.sub('', cleaned_output)  # Entfernt Ollama-spezifische Sequenzen
    cleaned_output = LOADING_CHARS_REGEX.sub('', cleaned_output)  # Entfernt Ladeanimationszeichen
    cleaned_output = CARRIAGE_RETURN_REGEX.sub('', cleaned_output)  # Entfernt Wagenrücklaufzeichen
    cleaned_output = CUSTOM_TEXT_REGEX.sub('', cleaned_output)  # Entfernt benutzerdefinierten Text
    return cleaned_output

def format_as_codeblock(output: str) -> str:
    """
    Verpackt den gesamten Output in einen Markdown-Codeblock.

    Args:
        output (str): Der Text, der formatiert werden soll.

    Returns:
        str: Der formatierte Text als Markdown-Codeblock.
    """
    return f"```\n{output}\n```"

# =============================================================================
# Funktion zur Ausführung von Ollama mit Live-Ausgabe
# =============================================================================

def run_ollama_live(prompt: str, model: str):
    """
    Führt den Ollama-Prozess mit dem gewählten Modell aus und gibt die Ausgabe live zeilenweise zurück.

    Args:
        prompt (str): Die Eingabeaufforderung für Ollama.
        model (str): Das zu verwendende Modell.

    Yields:
        str: Die aktuelle Ausgabe als Markdown-Codeblock.
    """
    try:
        # Startet den Ollama-Prozess
        process = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding='utf-8',
        )

        # Sendet die Eingabeaufforderung an Ollama
        process.stdin.write(prompt + "\n")
        process.stdin.close()

        buffer = ""
        # Liest die Ausgabe zeilenweise
        for line in iter(process.stdout.readline, ''):
            clean_line = clean_output(line)  # Bereinigt die Zeile
            if clean_line:
                buffer += clean_line + "\n"  # Fügt die Zeile dem Puffer hinzu
                yield format_as_codeblock(buffer)  # Gibt die aktuelle Antwort aus

        process.stdout.close()
        process.wait()  # Wartet auf das Ende des Prozesses

    except Exception as e:
        # Gibt eine Fehlermeldung zurück, falls ein Fehler auftritt
        yield f"**Fehler:** {str(e)}"

# =============================================================================
# Funktion zur Verarbeitung von hochgeladenen Dateien
# =============================================================================

def process_uploaded_file(file):
    """
    Liest den Inhalt von TXT- und PDF-Dateien.

    Args:
        file: Die hochgeladene Datei.

    Returns:
        str: Der Inhalt der Datei als Text.

    Raises:
        ValueError: Wenn das Dateiformat nicht unterstützt wird.
    """
    if file.name.endswith(".txt"):
        # Öffnet und liest eine Textdatei
        with open(file.name, 'r', encoding='utf-8') as f:
            content = f.read()
    elif file.name.endswith(".pdf"):
        # Öffnet und liest eine PDF-Datei
        reader = PdfReader(file.name)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
    else:
        # Unterstützt nur TXT- und PDF-Dateien
        raise ValueError("Nur TXT- und PDF-Dateien werden unterstützt.")
    return content

# =============================================================================
# Gradio-Interface Funktion
# =============================================================================

def chatbot_interface(input_text, model, file):
    """
    Verarbeitet Benutzereingaben oder hochgeladene Dateien, führt Ollama live aus und gibt die Antwort zeilenweise zurück.

    Args:
        input_text (str): Der vom Benutzer eingegebene Text.
        model (str): Das ausgewählte Modell.
        file: Die hochgeladene Datei (optional).

    Yields:
        tuple: Die aktuelle Antwort und der Status.
    """
    yield "", STATUS_MESSAGE_GENERATING  # Zeigt den initialen Status an

    # Überprüft, ob eine Datei hochgeladen wurde
    if file:
        try:
            input_text = process_uploaded_file(file)  # Extrahiert den Text aus der Datei
        except Exception as e:
            # Gibt eine Fehlermeldung zurück, falls die Datei nicht verarbeitet werden kann
            yield f"**Fehler beim Verarbeiten der Datei:** {str(e)}", STATUS_MESSAGE_ERROR
            return

    try:
        # Führt Ollama aus und gibt die Antwort live zurück
        for chunk in run_ollama_live(input_text, model):
            yield chunk, STATUS_MESSAGE_GENERATING

        yield chunk, STATUS_MESSAGE_COMPLETE  # Zeigt an, dass die Antwort vollständig ist

    except Exception:
        # Gibt einen Fehlerstatus zurück, falls etwas schiefgeht
        yield "", STATUS_MESSAGE_ERROR

# =============================================================================
# Erstellung der Gradio-App
# =============================================================================

# Definiert das Benutzerinterface mit den Eingaben und Ausgaben
interface = gr.Interface(
    fn=chatbot_interface,
    inputs=[
        gr.Textbox(
            lines=2, 
            placeholder="Geben Sie Ihre Frage an Ollama ein", 
            label="Eingabe (oder Datei hochladen)"
        ),
        gr.Dropdown(
            choices=MODELS, 
            value=DEFAULT_MODEL, 
            label="Modell auswählen"
        ),
        gr.File(
            label="Datei hochladen (PDF oder TXT)", 
            file_types=[".txt", ".pdf"]
        )
    ],
    outputs=[
        gr.Markdown(label="Antwort"),  # Zeigt die Antwort formatiert an
        gr.Label(label="Status")  # Zeigt den aktuellen Status an
    ],
    title="Ollama Gradio App mit Datei-Upload",
    description="Dieses Interface ermöglicht es, Dateien hochzuladen (PDF oder TXT), sie zu analysieren und Antworten von Ollama zu generieren."
)

# =============================================================================
# Start der Anwendung
# =============================================================================

if __name__ == "__main__":
    # Startet die Gradio-App und macht sie öffentlich zugänglich
    interface.launch(share=True)
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
