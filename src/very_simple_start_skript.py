# very_simple_start_skript.py

import os
import subprocess
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Callable

def get_topics_from_env():
    ntfy_topics = os.environ.get("NTFY_TOPICS")
    if ntfy_topics:
        topics = ntfy_topics.split(',')
    else:
        topic = os.environ.get("NTFY_TOPIC")
        if topic:
            topics = [topic]
        else:
            raise ValueError("No NTFY_TOPIC or NTFY_TOPICS provided. At least one topic is required.")
    return topics

def run_ntfy(topic, client_script):
    print(f"Subscribing to topic: {topic}")

    debug = os.environ.get("DEBUG", "false")
    ntfy_cmd = f"ntfy --debug subscribe {topic} 'sh -c \"DEBUG={debug} python3 -u {client_script}\"'"

    process = subprocess.Popen(ntfy_cmd, shell=True)

    process.wait()

def main(run_function: Optional[Callable] = None, use_multiprocessing: bool = True):
    print("very-simple-start-skript.py is running...")
    print('Start Message System...')

    client_script = os.path.join('.', 'very_simple_instance.py')

    try:
        topics = get_topics_from_env()
    except ValueError as e:
        print(f"Error: {e}")
        return

    if run_function is None:
        run_function = run_ntfy

    processes = []
    if use_multiprocessing:
        for topic in topics:
            process = multiprocessing.Process(target=run_function, args=(topic, client_script))
            processes.append(process)
            process.start()

        # Wait for all run_ntfy calls to complete
        for process in processes:
            process.join()
    else:
        for topic in topics:
            run_function(topic, client_script)

if __name__ == "__main__":
    main()
