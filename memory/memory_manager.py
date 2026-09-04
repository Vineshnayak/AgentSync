import sqlite3
import os
from utils.logging_config import setup_logger

logger = setup_logger("memory_manager")

class MemoryManager:
    def __init__(self, db_path="agentsync_memory.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workflow_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_request TEXT,
                    plan TEXT,
                    research_results TEXT,
                    analysis TEXT,
                    decision TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to initialize memory DB: {e}")

    def save_workflow(self, state: dict):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO workflow_history 
                (user_request, plan, research_results, analysis, decision) 
                VALUES (?, ?, ?, ?, ?)
            ''', (
                state.get("user_request", ""),
                state.get("plan", ""),
                state.get("research_results", ""),
                state.get("analysis", ""),
                state.get("decision", "")
            ))
            conn.commit()
            conn.close()
            logger.info("Saved workflow to long-term memory.")
        except Exception as e:
            logger.error(f"Failed to save to memory DB: {e}")

    def get_past_decisions(self, keyword: str):
        """Retrieve past decisions related to a keyword to avoid redundant work."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_request, decision FROM workflow_history 
                WHERE user_request LIKE ? ORDER BY timestamp DESC LIMIT 3
            ''', (f"%{keyword}%",))
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Failed to retrieve from memory DB: {e}")
            return []

memory_manager = MemoryManager()
