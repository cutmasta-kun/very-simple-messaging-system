import json
import os
import requests

# Lesen Sie die Umgebungsvariablen von ntfy
message_id = os.environ["NTFY_ID"]
message_time = os.environ["NTFY_TIME"]
message_topic = os.environ["NTFY_TOPIC"]
message_body = os.environ["NTFY_MESSAGE"]
message_title = os.environ["NTFY_TITLE"]
message_priority = os.environ["NTFY_PRIORITY"]
message_tags = os.environ["NTFY_TAGS"]
message_raw = os.environ["NTFY_RAW"]

# Erstellen Sie eine JSON-Datei aus der empfangenen Nachricht
message_data = {
    "id": message_id,
    "time": message_time,
    "topic": message_topic,
    "message": message_body,
    "title": message_title,
    "priority": message_priority,
    "tags": message_tags.split(','),  # Konvertieren Sie die kommaseparierte Liste in ein Array
    "raw": json.loads(message_raw)    # Laden Sie die Roh-JSON-Nachricht als Python-Objekt
}

print(message_data)

filename = f"{message_id}.json"

# Speichern Sie die JSON-Datei in einer temporären Datei
with open(filename, "w") as json_file:
    json.dump(message_data, json_file)

# URL des very-simple-upload-server
upload_url = "http://very-simple-upload-server:80"

# Übertragen Sie die JSON-Datei an den very-simple-upload-server
with open(filename, "rb") as json_file:
    response = requests.put(f"{upload_url}/{message_topic}/{filename}", files={"file": json_file})

# Entfernen Sie die temporäre Datei
os.remove(filename)