#!/usr/bin/env python3
"""
Database initialization and migration script.

This script initializes the database with the proper schema based on
SQLAlchemy models. It supports both SQLite (development) and MySQL (production).

Usage:
    python init_db.py          # Initialize database with default schema
    python init_db.py --reset  # Reset database (WARNING: deletes all data)
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(Path(__file__).parent, 'src'))

from database import engine, init_db, SessionLocal
from models import Base, Activity, User


def initialize_database():
    """Create all tables in the database."""
    print("🔄 Initializing database...")
    try:
        init_db(Base)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False


def reset_database():
    """Drop all tables and recreate them. WARNING: This deletes all data!"""
    print("⚠️  WARNING: This will delete all data from the database!")
    response = input("Are you sure? (yes/no): ")
    
    if response.lower() != "yes":
        print("❌ Operation cancelled.")
        return False
    
    try:
        print("🔄 Resetting database...")
        Base.metadata.drop_all(bind=engine)
        init_db(Base)
        print("✅ Database reset successfully!")
        return True
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        return False


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        initialize_database()


if __name__ == "__main__":
    main()
