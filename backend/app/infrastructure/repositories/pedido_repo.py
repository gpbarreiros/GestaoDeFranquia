from sqlalchemy.orm import Session, joinedload
from app.domain.models.pedido import Pedido, ItemPedido
from app.domain.enums import StatusPedidoEnum, CanalPedidoEnum
import uuid


def criar(db: Session, pedido: Pedido) -> Pedido:
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


def buscarPorId(db: Session, pedidoId: uuid.UUID) -> Pedido | None:
    return (
        db.query(Pedido)
        .options(joinedload(Pedido.itens))
        .filter(Pedido.id == pedidoId)
        .first()
    )


def listar(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    status: StatusPedidoEnum | None = None,
    canalPedido: CanalPedidoEnum | None = None,
    clienteId: uuid.UUID | None = None,
    unidadeId: uuid.UUID | None = None,
) -> list[Pedido]:
    query = db.query(Pedido).options(joinedload(Pedido.itens))

    if status:
        query = query.filter(Pedido.status == status)
    if canalPedido:
        query = query.filter(Pedido.canalPedido == canalPedido)
    if clienteId:
        query = query.filter(Pedido.clienteId == clienteId)
    if unidadeId:
        query = query.filter(Pedido.unidadeId == unidadeId)

    return query.order_by(Pedido.criadoEm.desc()).offset(skip).limit(limit).all()


def atualizar(db: Session, pedido: Pedido) -> Pedido:
    db.commit()
    db.refresh(pedido)
    return pedido