from fastapi import APIRouter, Request
from app.api.deps import DbDep, UsuarioAtualDep
from app.schemas.pagamento import PagamentoCreate, PagamentoResponse
from app.application import pagamento_service

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.post("", response_model=PagamentoResponse, status_code=201)
def processar(
    dados: PagamentoCreate,
    request: Request,
    db: DbDep,
    usuario: UsuarioAtualDep,
):
    ip = request.client.host if request.client else None
    return pagamento_service.processar(db, dados.pedidoId, dados.forma, usuario, ip)