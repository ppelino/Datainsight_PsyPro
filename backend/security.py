from datetime import datetime, timedelta
from typing import Optional
import os

from jose import jwt, JWTError
from passlib.hash import pbkdf2_sha256
from passlib.exc import UnknownHashError

# Usa o segredo do Render (Environment Variable NR01_SECRET)
SECRET_KEY = os.environ.get("NR01_SECRET", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 horas


def hash_password(password: str) -> str:
    """Gera o hash da senha usando pbkdf2_sha256 (mesmo formato do Supabase)."""
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Confere se a senha em texto puro bate com o hash armazenado."""
    try:
        return pbkdf2_sha256.verify(password, password_hash)
    except UnknownHashError:
        # Se o hash tiver formato estranho, tratamos como senha inválida
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um JWT com prazo de expiração.
    `data` normalmente vai ter pelo menos {"sub": user_id}.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


