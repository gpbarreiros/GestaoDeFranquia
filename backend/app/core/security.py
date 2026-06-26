from datetime import datetime, timedelta, timezone
from typing import Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashSenha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificarSenha(senha: str, senhaHash: str) -> bool:
    return pwd_context.verify(senha, senhaHash)


def criarAccessToken(dados: dict[str, Any]) -> str:
    payload = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=settings.accessTokenExpireMinutes
    )
    payload.update({"exp": expiracao})
    return jwt.encode(payload, settings.secretKey, algorithm=settings.algorithm)


def decodificarToken(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token,
            settings.secretKey,
            algorithms=[settings.algorithm],
        )
        return payload
    except JWTError:
        return None