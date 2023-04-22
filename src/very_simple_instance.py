# very_simple_instance.py

import json
import os
import requests

def on_message(topic, payload):
    print(f"Message received: {topic} {payload}")  # Diese Zeile hinzufügen, um die empfangene Nachricht auszugeben

def process_message(message_data):
    message_id = message_data["NTFY_ID"]
    message_time = message_data["NTFY_TIME"]
    message_topic = message_data["NTFY_TOPIC"]
    message_body = message_data["NTFY_MESSAGE"]
    message_title = message_data["NTFY_TITLE"]
    message_priority = message_data["NTFY_PRIORITY"]
    message_tags = message_data["NTFY_TAGS"]
    message_raw = message_data["NTFY_RAW"]


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

    # Überprüfen Sie den DEBUG Wert und drucken Sie die Nachricht nur, wenn DEBUG auf true gesetzt ist
    debug = os.environ.get("DEBUG", "false")
    if debug.lower() == "true":
        print(message_data)

        # Rufen Sie die on_message-Funktion auf
        on_message(message_data["topic"], message_data["message"])

    filename = f"{message_id}.json"

    # Speichern Sie die JSON-Datei in einer temporären Datei
    with open(filename, "w") as json_file:
        json.dump(message_data, json_file)

    # URL des very-simple-upload-server
    upload_url = "http://very-simple-upload-server:80"

    if debug.lower() == "true":
        print(f"Uploading file {filename} to {upload_url}/{message_topic}/{filename}")

    with open(filename, "rb") as json_file:
        response = requests.put(f"{upload_url}/{message_topic}/{filename}", files={"file": json_file})

    if debug.lower() == "true":
        print(f"File uploaded. Response status code: {response.status_code}")

    # Entfernen Sie die temporäre Datei
    os.remove(filename)

if __name__ == "__main__":
    message_data = {
        "NTFY_ID": os.environ["NTFY_ID"],
        "NTFY_TIME": os.environ["NTFY_TIME"],
        "NTFY_TOPIC": os.environ["NTFY_TOPIC"],
        "NTFY_MESSAGE": os.environ["NTFY_MESSAGE"],
        "NTFY_TITLE": os.environ["NTFY_TITLE"],
        "NTFY_PRIORITY": os.environ["NTFY_PRIORITY"],
        "NTFY_TAGS": os.environ["NTFY_TAGS"],
        "NTFY_RAW": os.environ["NTFY_RAW"],
    }
    process_message(message_data)
