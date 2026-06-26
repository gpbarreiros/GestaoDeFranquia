from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.core.security import decodificarToken
from app.domain.models.usuario import Usuario
from app.domain.enums import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

DbDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_usuario_atual(token: TokenDep, db: DbDep) -> Usuario:
    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error": "NAO_AUTENTICADO",
            "message": "Token inválido ou expirado.",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decodificarToken(token)
    if payload is None:
        raise credenciais_exception

    usuarioId: str = payload.get("sub")
    if usuarioId is None:
        raise credenciais_exception

    usuario = db.query(Usuario).filter(
        Usuario.id == usuarioId,
        Usuario.ativo == True,
    ).first()

    if usuario is None:
        raise credenciais_exception

    return usuario


UsuarioAtualDep = Annotated[Usuario, Depends(get_usuario_atual)]


def requer_role(*roles: RoleEnum):
    def verificar(usuario: UsuarioAtualDep) -> Usuario:
        if usuario.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "SEM_PERMISSAO",
                    "message": f"Acesso restrito. Perfil necessário: {[r.value for r in roles]}",
                },
            )
        return usuario
    return Depends(verificar)