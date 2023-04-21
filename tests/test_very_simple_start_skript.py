# test_very_simple_start_skript.py

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch
from very_simple_start_skript import get_topics_from_env

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

# (Restliche Tests wie test_run_ntfy())

if __name__ == "__main__":
    unittest.main()
