import uuid
from typing import Optional
from sqlalchemy import Integer, String, DateTime, ForeignKey, func, UniqueConstraint, CheckConstraint, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base
from app.domain.enums import TipoMovimentacaoFidelidadeEnum


class Fidelidade(Base):
    __tablename__ = "fidelidade"
    __table_args__ = (
        UniqueConstraint("cliente_id", name="uq_fidelidade_cliente"),
        CheckConstraint("pontos_saldo >= 0", name="ck_fidelidade_saldo_positivo"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    clienteId: Mapped[uuid.UUID] = mapped_column(
        "cliente_id",
        UUID(as_uuid=True),
        ForeignKey("usuario.id", ondelete="CASCADE"),
        nullable=False,
    )
    pontosSaldo: Mapped[int] = mapped_column(
        "pontos_saldo",
        Integer,
        default=0,
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
        "Usuario", back_populates="fidelidade",
    )
    movimentacoes: Mapped[list["MovimentacaoFidelidade"]] = relationship(
        "MovimentacaoFidelidade",
        back_populates="fidelidade",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Fidelidade clienteId={self.clienteId} pontosSaldo={self.pontosSaldo}>"


class MovimentacaoFidelidade(Base):
    __tablename__ = "movimentacao_fidelidade"
    __table_args__ = (
        CheckConstraint("pontos >= 1", name="ck_movimentacao_fidelidade_pontos_minimo"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    fidelidadeId: Mapped[uuid.UUID] = mapped_column(
        "fidelidade_id",
        UUID(as_uuid=True),
        ForeignKey("fidelidade.id", ondelete="CASCADE"),
        nullable=False,
    )
    pedidoId: Mapped[Optional[uuid.UUID]] = mapped_column(
        "pedido_id",
        UUID(as_uuid=True),
        ForeignKey("pedido.id", ondelete="SET NULL"),
        nullable=True,
    )
    tipo: Mapped[TipoMovimentacaoFidelidadeEnum] = mapped_column(
        SAEnum(TipoMovimentacaoFidelidadeEnum, name="tipo_movimentacao_fidelidade_enum"),
        nullable=False,
    )
    pontos: Mapped[int] = mapped_column(Integer, nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    criadoEm: Mapped[DateTime] = mapped_column(
        "criado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    fidelidade: Mapped["Fidelidade"] = relationship(
        "Fidelidade", back_populates="movimentacoes",
    )
    pedido: Mapped[Optional["Pedido"]] = relationship(
        "Pedido", back_populates="movimentacoesFidelidade",
    )

    def __repr__(self) -> str:
        return f"<MovimentacaoFidelidade tipo={self.tipo} pontos={self.pontos}>"