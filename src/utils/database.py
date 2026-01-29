import sqlite3
from threading import Lock
from .logger import get_logger

logger = get_logger(__name__)

class DatabaseConnection:
    _instance = None
    _lock = Lock()  # Thread-safe singleton

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                logger.info("Initializing unique Database Connection (Singleton)")
                cls._instance = super(DatabaseConnection, cls).__new__(cls)
                cls._instance.connection = sqlite3.connect('dbs/events_management.db', check_same_thread=False)
        return cls._instance

    def get_connection(self):
        return self.connection