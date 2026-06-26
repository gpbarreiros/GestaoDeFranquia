import uuid
from fastapi import APIRouter, Request
from app.api.deps import DbDep, UsuarioAtualDep, requer_role
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoStatusUpdate
from app.application import pedido_service
from app.domain.enums import RoleEnum, StatusPedidoEnum, CanalPedidoEnum

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", response_model=PedidoResponse, status_code=201)
def criar(
    dados: PedidoCreate,
    request: Request,
    db: DbDep,
    usuario: UsuarioAtualDep,
):
    ip = request.client.host if request.client else None
    return pedido_service.criar(db, dados, usuario, ip)


@router.get("", response_model=list[PedidoResponse])
def listar(
    db: DbDep,
    usuario: UsuarioAtualDep,
    skip: int = 0,
    limit: int = 10,
    status: StatusPedidoEnum | None = None,
    canalPedido: CanalPedidoEnum | None = None,
    unidadeId: uuid.UUID | None = None,
):
    clienteId = (
        usuario.id
        if usuario.role == RoleEnum.CLIENTE
        else None
    )
    return pedido_service.listar(
        db,
        skip=skip,
        limit=limit,
        status=status,
        canalPedido=canalPedido,
        clienteId=clienteId,
        unidadeId=unidadeId,
    )


@router.get("/{pedidoId}", response_model=PedidoResponse)
def buscar(pedidoId: uuid.UUID, db: DbDep, _: UsuarioAtualDep):
    return pedido_service.buscarPorId(db, pedidoId)


@router.patch("/{pedidoId}/status", response_model=PedidoResponse)
def atualizarStatus(
    pedidoId: uuid.UUID,
    dados: PedidoStatusUpdate,
    request: Request,
    db: DbDep,
    usuario=requer_role(
        RoleEnum.ADMIN, RoleEnum.GERENTE,
        RoleEnum.COZINHA, RoleEnum.ATENDENTE,
    ),
):
    ip = request.client.host if request.client else None
    return pedido_service.atualizarStatus(db, pedidoId, dados, usuario, ip)