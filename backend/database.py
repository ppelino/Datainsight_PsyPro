import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔴 COLE AQUI sua URL COMPLETA do Supabase:
# Exemplo (NÃO use esse, use o seu):
# "postgresql+psycopg://postgres.cpjjeltdtrtqxldjzdnh:MINHA_NOVA_SENHA@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"

DATABASE_URL = "postgresql+psycopg://SEU_USUARIO:SUA_SENHA@SEU_HOST:6543/postgres"

# ✅ Se quiser, pode deixar essa leitura da env por cima:
# DATABASE_URL = os.environ.get("DATABASE_URL", DATABASE_URL)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


