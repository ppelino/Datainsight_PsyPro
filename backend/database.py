import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não configurada nas variáveis de ambiente do Render.")

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"} if "sslmode=require" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """
    Cria as tabelas no banco (users, campaigns, dimensions, responses).
    """
    # IMPORTANTE: garantir que os models foram importados
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
