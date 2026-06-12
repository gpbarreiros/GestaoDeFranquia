import uuid
from typing import Optional
from sqlalchemy import String, DateTime, Numeric, ForeignKey, func, CheckConstraint, Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base
from app.domain.enums import CanalPedidoEnum, StatusPedidoEnum


class Pedido(Base):
    __tablename__ = "pedido"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    clienteId: Mapped[uuid.UUID] = mapped_column(
        "cliente_id",
        UUID(as_uuid=True),
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False,
    )
    unidadeId: Mapped[uuid.UUID] = mapped_column(
        "unidade_id",
        UUID(as_uuid=True),
        ForeignKey("unidade.id", ondelete="RESTRICT"),
        nullable=False,
    )
    canalPedido: Mapped[CanalPedidoEnum] = mapped_column(
        "canal_pedido",
        SAEnum(CanalPedidoEnum, name="canal_pedido_enum"),
        nullable=False,
    )
    status: Mapped[StatusPedidoEnum] = mapped_column(
        SAEnum(StatusPedidoEnum, name="status_pedido_enum"),
        default=StatusPedidoEnum.AGUARDANDO_PAGAMENTO,
        nullable=False,
    )
    total: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
        nullable=False,
    )
    observacao: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    criadoEm: Mapped[DateTime] = mapped_column(
        "criado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    atualizadoEm: Mapped[DateTime] = mapped_column(
        "atualizado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    cliente: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="pedidos",
        foreign_keys=[clienteId],
    )
    unidade: Mapped["Unidade"] = relationship(
        "Unidade", back_populates="pedidos",
    )
    itens: Mapped[list["ItemPedido"]] = relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan",
    )
    pagamento: Mapped[Optional["Pagamento"]] = relationship(
        "Pagamento",
        back_populates="pedido",
        uselist=False,
    )
    movimentacoesFidelidade: Mapped[list["MovimentacaoFidelidade"]] = relationship(
        "MovimentacaoFidelidade",
        back_populates="pedido",
    )

    def __repr__(self) -> str:
        return f"<Pedido id={self.id} status={self.status} total={self.total}>"


class ItemPedido(Base):
    __tablename__ = "item_pedido"
    __table_args__ = (
        CheckConstraint("quantidade >= 1", name="ck_item_pedido_quantidade_minima"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    pedidoId: Mapped[uuid.UUID] = mapped_column(
        "pedido_id",
        UUID(as_uuid=True),
        ForeignKey("pedido.id", ondelete="CASCADE"),
        nullable=False,
    )
    produtoId: Mapped[uuid.UUID] = mapped_column(
        "produto_id",
        UUID(as_uuid=True),
        ForeignKey("produto.id", ondelete="RESTRICT"),
        nullable=False,
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    precoUnitario: Mapped[float] = mapped_column(
        "preco_unitario",
        Numeric(10, 2),
        nullable=False,
    )
    subtotal: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    pedido: Mapped["Pedido"] = relationship(
        "Pedido", back_populates="itens",
    )
    produto: Mapped["Produto"] = relationship(
        "Produto", back_populates="itensPedido",
    )

    def __repr__(self) -> str:
        return f"<ItemPedido pedidoId={self.pedidoId} produtoId={self.produtoId} quantidade={self.quantidade}>"