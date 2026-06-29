from datetime import datetime, timedelta, timezone
from typing import Any
import bcrypt
from jose import JWTError, jwt
from app.core.config import settings

SIZE_MAXIMO = 72


def hashSenha(senha: str) -> str:
    senhaBytes = senha.encode("utf-8")[:SIZE_MAXIMO]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senhaBytes, salt).decode("utf-8")


def verificarSenha(senha: str, senhaHash: str) -> bool:
    senhaBytes = senha.encode("utf-8")[:SIZE_MAXIMO]
    return bcrypt.checkpw(senhaBytes, senhaHash.encode("utf-8"))


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