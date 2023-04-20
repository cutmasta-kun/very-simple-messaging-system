import os
import subprocess

print('Start Message System...')

# Setzen Sie den Pfad für das very-simple-upload-server-client.py Skript
client_script = "./very-simple-upload-server-client.py"

# Setzen Sie das ntfy-Topic, für das Sie sich anmelden möchten
topic = os.environ["NTFY_TOPIC"]

# Erstellen Sie den Befehl für die ntfy-Sub-Instanz
ntfy_cmd = f"ntfy subscribe {topic} 'python3 {client_script}'"

# Starten Sie die ntfy-Sub-Instanz
subprocess.run(ntfy_cmd, shell=True)
