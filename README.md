# Very Simple Messaging System  

Dieses Projekt stellt ein einfaches Messaging-System zur Verfügung, das auf `ntfy.sh` basiert und einen `very-simple-upload-server` verwendet, um Nachrichten als JSON-Dateien zu speichern. Die Anwendung besteht aus zwei Docker-Containern, die mit `docker-compose` orchestriert werden.  
## Features 

- Verwendung von `ntfy.sh` für Publish/Subscribe-Messaging 
- Speichern von JSON-Nachrichten als Dateien mit `very-simple-upload-server`
- Python-Skripte zum Verarbeiten ankommender Nachrichten 
- Einfache Installation und Konfiguration mit Docker 
- Debug-Modus für detaillierte Informationen während der Entwicklung

## Anforderungen  

- Docker 
- docker-compose  

## Installation und Start  

1. Klonen Sie dieses Repository:
   ```bash
   git clone https://github.com/yourusername/very-simple-messaging-system.git 
   cd very-simple-messaging-system
   ```

2.  Starten Sie die Docker-Container mit `docker-compose`:
```bash
docker-compose up -d
```

3.  Öffnen Sie die Anwendung im Browser oder verwenden Sie cURL, um Nachrichten zu senden.

## Verwendung

Die `very-simple-messaging-app` verwendet Python-Skripte, um auf eingehende Nachrichten zu reagieren. Wenn eine Nachricht empfangen wird, führt das Skript eine Aktion aus und speichert die JSON-Nachricht als Datei auf dem `very-simple-upload-server`.

## Anpassung und Erweiterung

Sie können dieses Projekt anpassen und erweitern, indem Sie die Python-Skripte in `./src/commands` ändern oder eigene Skripte hinzufügen. Stellen Sie sicher, dass die Skripte korrekt auf die API des `very-simple-upload-server` zugreifen, um die ankommenden JSON-Nachrichten als Dateien zu speichern.

## Debug-Modus

Um den Debug-Modus zu aktivieren, setzen Sie die Umgebungsvariable `DEBUG` auf `true` in der `docker-compose.yaml` Datei. Dies zeigt zusätzliche Informationen während der Ausführung des Projekts an, die bei der Fehlersuche und Entwicklung hilfreich sein können.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen finden Sie in der [LICENSE](https://chat.openai.com/LICENSE)-Datei.