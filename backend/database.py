import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Exemplo de URL do Supabase:
# postgresql+psycopg2://usuario:senha@host:5432/postgres
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./local_dev.db"  # fallback p/ desenvolvimento
)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
