#!/usr/bin/env python3
"""
Database initialization script for WhatsApp Financial Bot
Run this script to create all necessary database tables
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from add_data_in_database import Base, engine, SessionLocal

def init_database():
    """Initialize database tables"""
    try:
        print("🔄 Initializing database...")
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        print("✅ Database tables created successfully!")
        print("📊 Tables created:")
        print("   - users")
        print("   - user_interactions")
        
        # Test database connection
        session = SessionLocal()
        try:
            # Simple test query
            from sqlalchemy import text
            result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = result.fetchall()
            print(f"📋 Available tables: {[table[0] for table in tables]}")
        except Exception as e:
            print(f"⚠️  Warning: Could not verify tables: {e}")
        finally:
            session.close()
            
        print("🎉 Database initialization complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
