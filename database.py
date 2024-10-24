import sqlite3
from sqlite3 import Error
import os
from config import SQLITE_DB_PATH

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    async def connect(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(SQLITE_DB_PATH)
            self.cursor = self.conn.cursor()
            self._create_tables()
            return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_ranks (
                    discord_id INTEGER PRIMARY KEY,
                    support_rank TEXT,
                    dps_rank TEXT,
                    tank_rank TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except Error as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()

    async def update_ranks(self, discord_id, support_rank, dps_rank, tank_rank):
        """Update or insert player ranks"""
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO player_ranks 
                (discord_id, support_rank, dps_rank, tank_rank, last_updated)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (discord_id, support_rank, dps_rank, tank_rank))
            self.conn.commit()
            return True
        except Error as e:
            print(f"Error updating ranks: {e}")
            self.conn.rollback()
            return False

    async def get_ranks(self, discord_id):
        """Get player ranks"""
        try:
            self.cursor.execute("""
                SELECT support_rank, dps_rank, tank_rank
                FROM player_ranks
                WHERE discord_id = ?
            """, (discord_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching ranks: {e}")
            return None

    def close(self):
        """Close database connections"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
