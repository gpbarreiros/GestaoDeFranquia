from fastapi import APIRouter, Request
from app.api.deps import DbDep, requer_role
from app.schemas.estoque import MovimentacaoEstoqueCreate, EstoqueResponse, MovimentacaoEstoqueResponse
from app.application import estoque_service
from app.domain.enums import RoleEnum
import uuid

router = APIRouter(prefix="/estoque", tags=["Estoque"])


@router.post("/movimentacoes", response_model=EstoqueResponse, status_code=201)
def movimentar(
    dados: MovimentacaoEstoqueCreate,
    request: Request,
    db: DbDep,
    usuario=requer_role(RoleEnum.ADMIN, RoleEnum.GERENTE, RoleEnum.ATENDENTE),
):
    ip = request.client.host if request.client else None
    return estoque_service.movimentar(db, dados, usuario, ip)


@router.get("/unidades/{unidadeId}", response_model=list[EstoqueResponse])
def consultarPorUnidade(
    unidadeId: uuid.UUID,
    db: DbDep,
    usuario=requer_role(RoleEnum.ADMIN, RoleEnum.GERENTE, RoleEnum.ATENDENTE),
):
    return estoque_service.consultarPorUnidade(db, unidadeId)