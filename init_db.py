"""
Database initialization script.
Run this once to set up the database tables.
"""
from app.database import init_database

if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    print("Database initialization complete!")

