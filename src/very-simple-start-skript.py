import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

print("very-simple-start-skript.py is running...")
print('Start Message System...')

client_script = os.path.join('.', 'very-simple-instance.py')  # Verwenden von os.path.join() für plattformübergreifende Kompatibilität

ntfy_topics = os.environ.get("NTFY_TOPICS")

if ntfy_topics:
    topics = ntfy_topics.split(',')
else:
    topic = os.environ.get("NTFY_TOPIC")
    if topic:
        topics = [topic]
    else:
        raise ValueError("No NTFY_TOPIC or NTFY_TOPICS provided. At least one topic is required.")

def run_ntfy(topic):
    print(f"Subscribing to topic: {topic}")

    debug = os.environ.get("DEBUG", "false")
    ntfy_cmd = f"ntfy --debug subscribe {topic} 'sh -c \"DEBUG={debug} python3 -u {client_script}\"'"

    process = subprocess.Popen(ntfy_cmd, shell=True)

    process.wait()

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(run_ntfy, topic) for topic in topics]
