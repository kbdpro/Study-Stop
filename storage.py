# -*- coding: utf-8 -*-
"""
Study Stop - Veri Depolama Modülü (Storage Module)
Kullanıcının eksik konularını ve test geçmişini yerel bir JSON dosyasında saklar.
"""

import os
import json
import uuid
from datetime import datetime

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DEFAULT_DATA_FILE = os.path.join(DEFAULT_DATA_DIR, "studystop_data.json")

class DataManager:
    def __init__(self, filepath=DEFAULT_DATA_FILE):
        self.filepath = filepath
        self._ensure_storage()

    def _ensure_storage(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            initial_data = {
                "topics": [],
                "history": [],
                "preferences": {
                    "language": "tr"
                }
            }
            self._save_data(initial_data)

    def _load_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"topics": [], "history": [], "preferences": {"language": "tr"}}

    def _save_data(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # --- Eksik Konular İşlemleri ---
    def get_topics(self):
        data = self._load_data()
        return data.get("topics", [])

    def add_topic(self, grade, subject, topic, note=""):
        data = self._load_data()
        new_topic = {
            "id": str(uuid.uuid4())[:8],
            "grade": grade.strip(),
            "subject": subject.strip(),
            "topic": topic.strip(),
            "note": note.strip(),
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "tests_completed": 0
        }
        data.setdefault("topics", []).append(new_topic)
        self._save_data(data)
        return new_topic

    def delete_topic(self, topic_id):
        data = self._load_data()
        data["topics"] = [t for t in data.get("topics", []) if t["id"] != topic_id]
        self._save_data(data)
        return True

    def get_topic_by_id(self, topic_id):
        topics = self.get_topics()
        for t in topics:
            if t["id"] == topic_id:
                return t
        return None

    def increment_topic_test_count(self, topic_id):
        data = self._load_data()
        for t in data.get("topics", []):
            if t["id"] == topic_id:
                t["tests_completed"] = t.get("tests_completed", 0) + 1
                break
        self._save_data(data)

    # --- Test Geçmişi İşlemleri ---
    def get_history(self):
        data = self._load_data()
        return data.get("history", [])

    def add_history_entry(self, topic, subject, grade, score, total):
        data = self._load_data()
        percentage = round((score / total) * 100) if total > 0 else 0
        entry = {
            "id": str(uuid.uuid4())[:8],
            "topic": topic,
            "subject": subject,
            "grade": grade,
            "score": score,
            "total": total,
            "percentage": percentage,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        data.setdefault("history", []).insert(0, entry)  # En yeni en başta
        self._save_data(data)
        return entry

    def clear_history(self):
        data = self._load_data()
        data["history"] = []
        self._save_data(data)

    # --- Tercihler ---
    def get_language(self):
        data = self._load_data()
        return data.get("preferences", {}).get("language", "tr")

    def set_language(self, lang):
        data = self._load_data()
        data.setdefault("preferences", {})["language"] = lang
        self._save_data(data)
