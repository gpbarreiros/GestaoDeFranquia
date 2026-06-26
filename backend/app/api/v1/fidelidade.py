import uuid
from fastapi import APIRouter
from app.api.deps import DbDep, UsuarioAtualDep
from app.schemas.fidelidade import FidelidadeResponse, ResgateRequest
from app.application import fidelidade_service

router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])


@router.get("/me", response_model=FidelidadeResponse)
def meuSaldo(usuario: UsuarioAtualDep, db: DbDep):
    return fidelidade_service.consultarSaldo(db, usuario.id)


@router.post("/resgatar", response_model=FidelidadeResponse)
def resgatar(
    dados: ResgateRequest,
    db: DbDep,
    usuario: UsuarioAtualDep,
):
    return fidelidade_service.resgatar(db, usuario.id, dados)