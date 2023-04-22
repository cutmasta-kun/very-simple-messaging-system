# test_very_simple_start_skript.py

import sys
import os
from typing import Optional, Callable

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch
from src.very_simple_start_skript import get_topics_from_env
from unittest.mock import MagicMock

class TestVerySimpleStartSkript(unittest.TestCase):
    def setUp(self):
        self.original_ntfy_topic = os.environ.get("NTFY_TOPIC")
        self.original_ntfy_topics = os.environ.get("NTFY_TOPICS")

    def tearDown(self):
        if self.original_ntfy_topic is not None:
            os.environ["NTFY_TOPIC"] = self.original_ntfy_topic
        else:
            os.environ.pop("NTFY_TOPIC", None)

        if self.original_ntfy_topics is not None:
            os.environ["NTFY_TOPICS"] = self.original_ntfy_topics
        else:
            os.environ.pop("NTFY_TOPICS", None)

    def test_get_topics_from_env_single_topic(self):
        os.environ["NTFY_TOPIC"] = "test_topic"
        if "NTFY_TOPICS" in os.environ:
            del os.environ["NTFY_TOPICS"]

        expected_topics = ["test_topic"]
        self.assertEqual(get_topics_from_env(), expected_topics)

    def test_get_topics_from_env_multiple_topics(self):
        os.environ["NTFY_TOPICS"] = "topic1,topic2,topic3"
        if "NTFY_TOPIC" in os.environ:
            del os.environ["NTFY_TOPIC"]

        expected_topics = ["topic1", "topic2", "topic3"]
        self.assertEqual(get_topics_from_env(), expected_topics)

    def test_get_topics_from_env_no_topics(self):
        if "NTFY_TOPIC" in os.environ:
            del os.environ["NTFY_TOPIC"]
        if "NTFY_TOPICS" in os.environ:
            del os.environ["NTFY_TOPICS"]

        with self.assertRaises(ValueError):
            get_topics_from_env()
    
    def test_main_multiple_topics(self):
        os.environ["NTFY_TOPICS"] = "topic1,topic2,topic3"
        if "NTFY_TOPIC" in os.environ:
            del os.environ["NTFY_TOPIC"]

        from src.very_simple_start_skript import main

        with unittest.mock.patch("src.very_simple_start_skript.run_ntfy") as mock_run_ntfy:
            main(run_function=mock_run_ntfy, use_multiprocessing=False)

        mock_run_ntfy.assert_has_calls([
            unittest.mock.call("topic1", unittest.mock.ANY),
            unittest.mock.call("topic2", unittest.mock.ANY),
            unittest.mock.call("topic3", unittest.mock.ANY),
        ])

    def test_main_single_topic(self):
        os.environ["NTFY_TOPIC"] = "test_topic"
        if "NTFY_TOPICS" in os.environ:
            del os.environ["NTFY_TOPICS"]

        from src.very_simple_start_skript import main

        with unittest.mock.patch("src.very_simple_start_skript.run_ntfy") as mock_run_ntfy:
            main(run_function=mock_run_ntfy, use_multiprocessing=False)

        mock_run_ntfy.assert_called_once_with("test_topic", unittest.mock.ANY)

    def test_main_no_topics(self):
        if "NTFY_TOPIC" in os.environ:
            del os.environ["NTFY_TOPIC"]
        if "NTFY_TOPICS" in os.environ:
            del os.environ["NTFY_TOPICS"]

        with unittest.mock.patch("very_simple_start_skript.run_ntfy") as mock_run_ntfy:
            with unittest.mock.patch("src.very_simple_start_skript.print") as mock_print:
                from src.very_simple_start_skript import main
                main()

            mock_print.assert_called_with("Error: No NTFY_TOPIC or NTFY_TOPICS provided. At least one topic is required.")
            mock_run_ntfy.assert_not_called()


    def test_main_default_run_function(self):
        os.environ["NTFY_TOPIC"] = "test_topic"
        if "NTFY_TOPICS" in os.environ:
            del os.environ["NTFY_TOPICS"]

        from src.very_simple_start_skript import main

        def mock_popen(cmd, shell):
            assert shell is True
            assert "ntfy --debug subscribe test_topic" in cmd
            assert f"DEBUG={os.environ.get('DEBUG', 'false')}" in cmd
            assert "python3 -u ./very_simple_instance.py" in cmd

            class MockProcess:
                def wait(self):
                    pass

            return MockProcess()

        with unittest.mock.patch("subprocess.Popen", side_effect=mock_popen):
            main(use_multiprocessing=False)

class TestVerySimpleStartSkriptWithMultiprocessing(unittest.TestCase):
    def setUp(self):
        self.original_ntfy_topic = os.environ.get("NTFY_TOPIC")
        self.original_ntfy_topics = os.environ.get("NTFY_TOPICS")

    def tearDown(self):
        if self.original_ntfy_topic is not None:
            os.environ["NTFY_TOPIC"] = self.original_ntfy_topic
        else:
            os.environ.pop("NTFY_TOPIC", None)

        if self.original_ntfy_topics is not None:
            os.environ["NTFY_TOPICS"] = self.original_ntfy_topics
        else:
            os.environ.pop("NTFY_TOPICS", None)

    @patch("multiprocessing.Process")
    def test_main_with_multiprocessing_single_topic(self, mock_process):
        os.environ["NTFY_TOPIC"] = "test_topic"
        if "NTFY_TOPICS" in os.environ:
            del os.environ["NTFY_TOPICS"]

        from src.very_simple_start_skript import main

        # Create a mock instance of Process
        process_instance = MagicMock()
        mock_process.return_value = process_instance

        main(run_function=None, use_multiprocessing=True)

        mock_process.assert_called_once_with(target=unittest.mock.ANY, args=("test_topic", unittest.mock.ANY))
        process_instance.start.assert_called_once()
        process_instance.join.assert_called_once()

    @patch("multiprocessing.Process")
    def test_main_with_multiprocessing_multiple_topics(self, mock_process):
        os.environ["NTFY_TOPICS"] = "topic1,topic2,topic3"
        if "NTFY_TOPIC" in os.environ:
            del os.environ["NTFY_TOPIC"]

        from src.very_simple_start_skript import main

        # Create a mock instance of Process
        process_instance = MagicMock()
        mock_process.return_value = process_instance

        main(run_function=None, use_multiprocessing=True)

        # Check if Process was called with the correct arguments
        calls = [
            unittest.mock.call(target=unittest.mock.ANY, args=("topic1", unittest.mock.ANY)),
            unittest.mock.call(target=unittest.mock.ANY, args=("topic2", unittest.mock.ANY)),
            unittest.mock.call(target=unittest.mock.ANY, args=("topic3", unittest.mock.ANY)),
        ]
        mock_process.assert_has_calls(calls, any_order=True)
        self.assertEqual(mock_process.call_count, 3)

        # Check if start() and join() were called on each process instance
        self.assertEqual(process_instance.start.call_count, 3)
        self.assertEqual(process_instance.join.call_count, 3)

class TestVerySimpleStartSkriptMainBlock(unittest.TestCase):
    def setUp(self):
        self.original_ntfy_topic = os.environ.get("NTFY_TOPIC")
        self.original_ntfy_topics = os.environ.get("NTFY_TOPICS")

    def tearDown(self):
        if self.original_ntfy_topic is not None:
            os.environ["NTFY_TOPIC"] = self.original_ntfy_topic
        else:
            os.environ.pop("NTFY_TOPIC", None)

        if self.original_ntfy_topics is not None:
            os.environ["NTFY_TOPICS"] = self.original_ntfy_topics
        else:
            os.environ.pop("NTFY_TOPICS", None)

    @patch("src.very_simple_start_skript.print")
    def test_main_value_error(self, mock_print):
        if "NTFY_TOPIC" in os.environ:
            del os.environ["NTFY_TOPIC"]
        if "NTFY_TOPICS" in os.environ:
            del os.environ["NTFY_TOPICS"]

        from src.very_simple_start_skript import main

        main(run_function=None, use_multiprocessing=True)

        mock_print.assert_called_with("Error: No NTFY_TOPIC or NTFY_TOPICS provided. At least one topic is required.")



if __name__ == "__main__":
    unittest.main()
