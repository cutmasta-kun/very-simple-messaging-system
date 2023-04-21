# test_instance.py

import os
import tempfile
import unittest.mock
from src.very_simple_instance import process_message

def test_process_message():
    example_message_data = {
        "NTFY_ID": "123",
        "NTFY_TIME": "2023-04-20T12:34:56Z",
        "NTFY_TOPIC": "test",
        "NTFY_MESSAGE": "This is a test message.",
        "NTFY_TITLE": "Test Message",
        "NTFY_PRIORITY": "low",
        "NTFY_TAGS": "test,example",
        "NTFY_RAW": '{"example_key": "example_value"}',
    }

    test_env = {
        "DEBUG": "false",
        "NTFY_ID": example_message_data["NTFY_ID"],
        "NTFY_TIME": example_message_data["NTFY_TIME"],
        "NTFY_TOPIC": example_message_data["NTFY_TOPIC"],
        "NTFY_MESSAGE": example_message_data["NTFY_MESSAGE"],
        "NTFY_TITLE": example_message_data["NTFY_TITLE"],
        "NTFY_PRIORITY": example_message_data["NTFY_PRIORITY"],
        "NTFY_TAGS": example_message_data["NTFY_TAGS"],
        "NTFY_RAW": example_message_data["NTFY_RAW"],
    }

    with unittest.mock.patch.dict(os.environ, test_env):
        with unittest.mock.patch("src.very_simple_instance.requests.put") as mock_put:
            mock_put.return_value = unittest.mock.MagicMock(status_code=200)

            with tempfile.TemporaryDirectory() as temp_dir:
                with unittest.mock.patch("src.very_simple_instance.os.remove") as mock_remove:
                    with unittest.mock.patch("src.very_simple_instance.open", unittest.mock.mock_open(), create=True) as mock_open:
                        process_message(example_message_data)

            mock_put.assert_called_once_with(
                "http://very-simple-upload-server:80/test/123.json",
                files={"file": unittest.mock.ANY},
            )

            # Überprüfen, ob die Datei erstellt und gelöscht wurde
            open_calls = [unittest.mock.call("123.json", "w"), unittest.mock.call("123.json", "rb")]
            mock_open.assert_has_calls(open_calls, any_order=True)

            mock_remove.assert_called_once_with("123.json")
