from sqlalchemy import create_engine
from backend.db.base import Base
from backend.core.config import settings

def create_tables():
    """Create all database tables."""
    engine = create_engine(f"sqlite:///{settings.DB_FILE}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    print(f"Database tables created successfully in {settings.DB_FILE}")

if __name__ == "__main__":
    create_tables()
