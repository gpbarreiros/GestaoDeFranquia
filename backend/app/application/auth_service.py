from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.infrastructure.repositories import usuario_repo
from app.core.security import verificarSenha, criarAccessToken
from app.core.config import settings


def login(db: Session, email: str, senha: str) -> dict:
    usuario = usuario_repo.buscarPorEmail(db, email)

    if not usuario or not verificarSenha(senha, usuario.senhaHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "CREDENCIAIS_INVALIDAS",
                "message": "E-mail ou senha inválidos.",
                "details": [],
            },
        )

    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "USUARIO_INATIVO",
                "message": "Usuário inativo. Entre em contato com o administrador.",
                "details": [],
            },
        )

    token = criarAccessToken({
        "sub": str(usuario.id),
        "role": usuario.role.value,
        "email": usuario.email,
    })

    return {
        "accessToken": token,
        "tokenType": "Bearer",
        "expiresIn": settings.accessTokenExpireMinutes * 60,
        "usuario": {
            "id": str(usuario.id),
            "nome": usuario.nome,
            "email": usuario.email,
            "role": usuario.role.value,
        },
    }