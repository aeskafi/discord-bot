import os
import tempfile
import unittest
from storage import LocalStorage
from main import parse_duration, get_quote, update_encouragements, delete_encouragement, SAD_WORDS, STARTER_ENCOURAGEMENTS
import main


class TestDiscordBot(unittest.TestCase):

    def test_local_storage(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            storage = LocalStorage(tmp_path)
            self.assertEqual(len(list(storage.keys())), 0)

            storage["test_key"] = "test_value"
            self.assertEqual(storage["test_key"], "test_value")
            self.assertIn("test_key", storage)
            self.assertEqual(storage.get("non_existent", "default"), "default")

            # Reload test
            storage2 = LocalStorage(tmp_path)
            self.assertEqual(storage2["test_key"], "test_value")

            del storage2["test_key"]
            self.assertNotIn("test_key", storage2)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_parse_duration(self):
        self.assertEqual(parse_duration("10s"), (10, "10 second(s)"))
        self.assertEqual(parse_duration("5m"), (300, "5 minute(s)"))
        self.assertEqual(parse_duration("2h"), (7200, "2 hour(s)"))
        self.assertEqual(parse_duration("1d"), (86400, "1 day(s)"))
        self.assertEqual(parse_duration("invalid"), (0, ""))
        self.assertEqual(parse_duration("10x"), (0, ""))
        self.assertEqual(parse_duration(""), (0, ""))

    def test_get_quote(self):
        quote = get_quote()
        self.assertIsInstance(quote, str)
        self.assertGreater(len(quote), 5)

    def test_encouragements_crud(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            test_storage = LocalStorage(tmp_path)
            main.db = test_storage

            self.assertEqual(main.db.get("encouragements", []), [])

            update_encouragements("Stay positive!")
            self.assertIn("Stay positive!", main.db["encouragements"])

            update_encouragements("Keep coding!")
            self.assertEqual(len(main.db["encouragements"]), 2)

            # Delete first
            success = delete_encouragement(0)
            self.assertTrue(success)
            self.assertEqual(len(main.db["encouragements"]), 1)
            self.assertEqual(main.db["encouragements"][0], "Keep coding!")

            # Delete invalid index
            fail = delete_encouragement(99)
            self.assertFalse(fail)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_sad_words_and_starters(self):
        self.assertGreaterEqual(len(SAD_WORDS), 5)
        self.assertGreaterEqual(len(STARTER_ENCOURAGEMENTS), 3)
        sample_text = "I am feeling so sad today"
        self.assertTrue(any(word in sample_text.lower().split() for word in SAD_WORDS))


if __name__ == "__main__":
    unittest.main()
