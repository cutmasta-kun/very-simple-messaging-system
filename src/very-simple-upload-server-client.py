import json
import os
import requests

# Lesen Sie die Umgebungsvariablen von ntfy
message_id = os.environ["NTFY_ID"]
message_time = os.environ["NTFY_TIME"]
message_topic = os.environ["NTFY_TOPIC"]
message_body = os.environ["NTFY_MESSAGE"]
message_priority = os.environ["NTFY_PRIORITY"]
message_raw = os.environ["NTFY_RAW"]

# Erstellen Sie eine JSON-Datei aus der empfangenen Nachricht
message_data = {
    "id": message_id,
    "time": message_time,
    "topic": message_topic,
    "message": message_body,
    "priority": message_priority,
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
