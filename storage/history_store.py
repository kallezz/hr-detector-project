import json

from config import Storage


class HistoryStore:
    """Keeps the last Storage.HISTORY_MAX_ENTRIES measurements, newest first.
    """

    def __init__(self, path=Storage.HISTORY_FILE):
        self._path = path

    def load(self):
        """Return the saved measurements, newest first.

        A missing, empty or broken file counts as no history.
        """
        try:
            with open(self._path) as history_file:
                records = json.load(history_file)
        except (OSError, ValueError):
            return []
        if not isinstance(records, list):
            return []
        return [record for record in records if isinstance(record, dict)]

    def save(self, record):
        records = self.load()
        records.insert(0, record)
        del records[Storage.HISTORY_MAX_ENTRIES:]
        with open(self._path, "w") as history_file:
            json.dump(records, history_file)