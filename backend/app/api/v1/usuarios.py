import uuid
from fastapi import APIRouter, Request
from app.api.deps import DbDep, UsuarioAtualDep, requer_role
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.application import usuario_service
from app.domain.enums import RoleEnum

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("", response_model=UsuarioResponse, status_code=201)
def criar(dados: UsuarioCreate, request: Request, db: DbDep):
    ip = request.client.host if request.client else None
    return usuario_service.criar(db, dados, ip)


@router.get("", response_model=list[UsuarioResponse])
def listar(
    db: DbDep,
    _: UsuarioAtualDep,
    skip: int = 0,
    limit: int = 10,
    admin=requer_role(RoleEnum.ADMIN),
):
    return usuario_service.listar(db, skip=skip, limit=limit)


@router.get("/me", response_model=UsuarioResponse)
def me(usuario: UsuarioAtualDep):
    return usuario


@router.get("/{usuarioId}", response_model=UsuarioResponse)
def buscar(
    usuarioId: uuid.UUID,
    db: DbDep,
    _: UsuarioAtualDep,
    admin=requer_role(RoleEnum.ADMIN),
):
    return usuario_service.buscarPorId(db, usuarioId)


@router.patch("/{usuarioId}", response_model=UsuarioResponse)
def atualizar(
    usuarioId: uuid.UUID,
    dados: UsuarioUpdate,
    request: Request,
    db: DbDep,
    usuario: UsuarioAtualDep,
    admin=requer_role(RoleEnum.ADMIN),
):
    ip = request.client.host if request.client else None
    return usuario_service.atualizar(db, usuarioId, dados, usuario, ip)