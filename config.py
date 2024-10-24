import os

# Rank definitions
VALID_RANKS = [
    'Bronze 5', 'Bronze 4', 'Bronze 3', 'Bronze 2', 'Bronze 1',
    'Silver 5', 'Silver 4', 'Silver 3', 'Silver 2', 'Silver 1',
    'Gold 5', 'Gold 4', 'Gold 3', 'Gold 2', 'Gold 1',
    'Platinum 5', 'Platinum 4', 'Platinum 3', 'Platinum 2', 'Platinum 1',
    'Diamond 5', 'Diamond 4', 'Diamond 3', 'Diamond 2', 'Diamond 1',
    'Master 5', 'Master 4', 'Master 3', 'Master 2', 'Master 1',
    'Grandmaster 5', 'Grandmaster 4', 'Grandmaster 3', 'Grandmaster 2', 'Grandmaster 1'
]

ROLES = ['Support', 'DPS', 'Tank']

# SQLite Database configuration
SQLITE_DB_PATH = 'ranks.db'
