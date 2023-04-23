# integration_test.py

import os
import requests
import unittest
import json
import uuid
import time
import subprocess
import sys
import shutil
import stat
import re
import docker

messaging_app_url = os.environ.get("NTFY_HOST", "https://ntfy.sh")
upload_server_url = "http://test_very-simple-upload-server:9090"  # Passen Sie die URL an Ihre Umgebung an
data_directory = "./data_test"
test_uuid = uuid.uuid4()
test_topic = os.environ.get("NTFY_TOPIC", uuid.uuid4())
test_message = f"test_message_with_uuid:{test_uuid}"
pre_tests_passed = False

def print_docker_compose_config():
    print("Printing docker-compose config...")

    env = {**os.environ,
           "TEST_NTFY_TOPIC": str(test_topic),
           "NTFY_HOST": messaging_app_url,
           "ENV_TEST": "### inside integration test docker compose info",
           "DEBUG": "true"}
    
    result = subprocess.run(
        [
            "docker-compose",
            "--file",
            "docker-compose.yaml",
            "--file",
            "docker-compose.override.test.yaml",
            "config"
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get docker-compose config: {result.stderr}")
    print(result.stdout)

def start_containers():
    print_docker_compose_config()
    print("Starting containers...")

    # Print environment variables
    print(f"NTFY_TOPIC: {test_topic}")
    print(f"NTFY_HOST: {messaging_app_url}")
    print(f"DEBUG: {'true'}")

    # Erstellen Sie das data_test-Verzeichnis, falls es nicht existiert
    os.makedirs(data_directory, exist_ok=True)

    env = {**os.environ,
           "TEST_NTFY_TOPIC": str(test_topic),
           "NTFY_HOST": messaging_app_url,
           "ENV_TEST": "### inside integration test",
           "DEBUG": "true"}

    print(f"TEST_NTFY_TOPIC: {env['TEST_NTFY_TOPIC']}")  # Debug-Ausgabe hinzufügen

    result = subprocess.run(
        [
            "docker-compose",
            "--file",
            "docker-compose.yaml",
            "--file",
            "docker-compose.override.test.yaml",
            "up",
            "-d",
            "--force-recreate",
        ],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to start containers: {result.stderr}")

    print("Containers started")

def stop_containers():
    print("Stopping containers...")
    result = subprocess.run(["docker-compose", "--file", "docker-compose.yaml", "--file", "docker-compose.override.test.yaml", "down"], capture_output=True, text=True)
 
    if result.returncode != 0:
        raise RuntimeError(f"Failed to stop containers: {result.stderr}")
    
    # Löschen des data_test-Verzeichnisses
    shutil.rmtree(data_directory, ignore_errors=True)

    # Löschen der docker-compose.override.test_updated.yaml Datei
    if os.path.exists("docker-compose.override.test_updated.yaml"):
        os.remove("docker-compose.override.test_updated.yaml")

    print("Containers stopped")

def wait_for_containers_healthcheck(max_wait_time=300):
    client = docker.from_env()
    container_names = [
        "very-simple-upload-server",
        "very-simple-messaging-app",
    ]
    healthy_containers = set()

    start_time = time.time()

    while len(healthy_containers) < len(container_names):
        for container_name in container_names:
            if container_name not in healthy_containers:
                container = client.containers.get(container_name)
                health_status = container.attrs["State"]["Health"]["Status"]
                print(health_status)
                if health_status == "healthy":
                    healthy_containers.add(container_name)
                    print(f"{container_name} is healthy")
                else:
                    print(f"Waiting for {container_name} to become healthy (current status: {health_status})")
                    container_logs = container.logs(tail=2).decode("utf-8")
                    print(f"Logs for {container_name}:\n{container_logs}")
        time.sleep(10)

        elapsed_time = time.time() - start_time
        if elapsed_time > max_wait_time:
            raise TimeoutError(f"Max wait time of {max_wait_time}s exceeded while waiting for containers to become healthy")

    print("All containers are healthy")

def wait_for_app_initialization(container_name, max_wait_time=30):
    client = docker.from_env()
    container = client.containers.get(container_name)

    start_time = time.time()

    for line in container.logs(stream=True, follow=True, since=int(start_time)):
        log_line = line.strip().decode('utf-8')
        print(log_line)
        if "very-simple-start-skript.py is running..." in log_line:
            print(f"{container_name} initialization detected")
            break

        elapsed_time = time.time() - start_time
        if elapsed_time > max_wait_time:
            raise TimeoutError(f"Max wait time of {max_wait_time}s exceeded while waiting for {container_name} initialization")

class PreIntegrationTest(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        global pre_tests_passed
        pre_tests_passed = True  # Diese Zeile wird nur ausgeführt, wenn alle Pre-Tests erfolgreich sind

    def test_docker(self):
        # Test, ob Docker installiert ist und ordnungsgemäß funktioniert
        try:
            version_output = subprocess.check_output(["docker", "--version"]).decode("utf-8").strip()
            print(f"Docker version: {version_output}")
        except (FileNotFoundError, subprocess.CalledProcessError):
            self.fail("Docker is not installed or not working properly")

    def test_docker_socket_permissions(self):
        # Test, ob die Berechtigungen für die Docker-Socket-Datei korrekt sind
        docker_socket_path = "/var/run/docker.sock"
        if os.path.exists(docker_socket_path):
            socket_stat = os.stat(docker_socket_path)
            if not socket_stat.st_mode & stat.S_IRUSR:
                self.fail("Docker socket does not have read permission for the owner")
            if not socket_stat.st_mode & stat.S_IWUSR:
                self.fail("Docker socket does not have write permission for the owner")
        else:
            self.fail("Docker socket not found")

    def test_dependencies(self):
        # Test, ob alle notwendigen Abhängigkeiten installiert sind
        dependencies = ["requests", "docker"]
        for dependency in dependencies:
            try:
                __import__(dependency)
            except ImportError:
                self.fail(f"Dependency '{dependency}' is not installed")

class IntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global pre_tests_passed
        if not pre_tests_passed:
            raise unittest.SkipTest("Skipping integration tests since pre-tests did not pass")
    def test_integration(self):
        print("Running integration test")
        try:
            start_containers()
            wait_for_containers_healthcheck()
        except (RuntimeError, TimeoutError) as e:
            self.fail(str(e))
        try:
            # Senden Sie die Testnachricht direkt an ntfy.sh
            ntfy_url = f"https://ntfy.sh/{test_topic}"
            print(f"Sending test message to {ntfy_url}")
            response = requests.post(ntfy_url, data=test_message.encode(encoding='utf-8'))
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()

            test_topic_directory = os.path.join(data_directory, str(test_topic))

            # Warten Sie, bis das Verzeichnis erstellt wird
            directory_created = False
            print(f"Waiting for directory {test_topic_directory} to be created...")

            for _ in range(20):  # Erhöhen Sie die Anzahl der Wiederholungen, um auf das Verzeichnis zu warten
                if os.path.exists(test_topic_directory):
                    directory_created = True
                    break
                time.sleep(2)  # Wartezeit in Sekunden

            self.assertTrue(directory_created, "Das Verzeichnis wurde nicht erstellt")

            # Warten Sie, bis die very-simple-messaging-app die Datei erstellt hat
            file_found = False
            message_id = None
            print(f"Checking for files in {test_topic_directory}...")

            for _ in range(10):  # Erhöhen Sie die Anzahl der Wiederholungen, um auf die Datei zu warten
                for file in os.listdir(test_topic_directory):
                    print(f"Found file: {file}")
                    if file.endswith(".json"):
                        with open(os.path.join(test_topic_directory, file), "r") as json_file:
                            file_content = json.load(json_file)
                            if file_content["message"] == test_message:
                                file_found = True
                                message_id = file[:-5]  # Extrahieren Sie die message_id aus dem Dateinamen (entfernen Sie ".json")
                                break
                if file_found:
                    break
                time.sleep(2)  # Wartezeit in Sekunden

            # Überprüfen Sie, ob die Datei gefunden wurde
            self.assertTrue(file_found, "Die Datei wurde nicht erstellt")

            # Überprüfen Sie, ob die Datei die erwarteten Daten enthält
            with open(os.path.join(test_topic_directory, f"{message_id}.json"), "r") as file:
                file_content = json.load(file)

            self.assertEqual(file_content["topic"], str(test_topic), "Das Testthema stimmt nicht überein")
            self.assertEqual(file_content["message"], test_message, "Die Testnachricht stimmt nicht überein")

        finally:
            stop_containers()

if __name__ == "__main__":
    unittest.main()
