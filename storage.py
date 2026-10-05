import os
import json
from typing import Any, List

class LocalStorage:
    """
    Lightweight, thread-safe JSON-backed dictionary storage.
    Provides identical interface to Replit DB for local & cloud environments.
    """
    def __init__(self, filepath: str = "database.json"):
        self.filepath = filepath
        self._data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def _save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Storage Warning] Failed to save database: {e}")

    def keys(self):
        return self._data.keys()

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any):
        self._data[key] = value
        self._save()

    def __delitem__(self, key: str):
        if key in self._data:
            del self._data[key]
            self._save()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)


def get_db():
    """
    Returns Replit DB if available in environment, otherwise local JSON-backed storage.
    """
    if os.getenv("REPLIT_DB_URL"):
        try:
            from replit import db
            return db
        except Exception:
            pass
    return LocalStorage()
