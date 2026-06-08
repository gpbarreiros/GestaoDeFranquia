import uuid
from typing import Optional
from sqlalchemy import Integer, String, DateTime, ForeignKey, func, UniqueConstraint, CheckConstraint, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base
from app.domain.enums import TipoMovimentacaoEstoqueEnum


class Estoque(Base):
    __tablename__ = "estoque"
    __table_args__ = (
        UniqueConstraint("unidade_id", "produto_id", name="uq_estoque_unidade_produto"),
        CheckConstraint("quantidade >= 0", name="ck_estoque_quantidade_positiva"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    unidadeId: Mapped[uuid.UUID] = mapped_column(
        "unidade_id",
        UUID(as_uuid=True),
        ForeignKey("unidade.id", ondelete="CASCADE"),
        nullable=False,
    )
    produtoId: Mapped[uuid.UUID] = mapped_column(
        "produto_id",
        UUID(as_uuid=True),
        ForeignKey("produto.id", ondelete="CASCADE"),
        nullable=False,
    )
    quantidade: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    atualizadoEm: Mapped[DateTime] = mapped_column(
        "atualizado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    unidade: Mapped["Unidade"] = relationship(
        "Unidade", back_populates="estoques",
    )
    produto: Mapped["Produto"] = relationship(
        "Produto", back_populates="estoques",
    )
    movimentacoes: Mapped[list["MovimentacaoEstoque"]] = relationship(
        "MovimentacaoEstoque",
        back_populates="estoque",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Estoque unidadeId={self.unidadeId} produtoId={self.produtoId} quantidade={self.quantidade}>"


class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacao_estoque"
    __table_args__ = (
        CheckConstraint("quantidade >= 1", name="ck_movimentacao_quantidade_minima"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    estoqueId: Mapped[uuid.UUID] = mapped_column(
        "estoque_id",
        UUID(as_uuid=True),
        ForeignKey("estoque.id", ondelete="CASCADE"),
        nullable=False,
    )
    tipo: Mapped[TipoMovimentacaoEstoqueEnum] = mapped_column(
        SAEnum(TipoMovimentacaoEstoqueEnum, name="tipo_movimentacao_estoque_enum"),
        nullable=False,
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    usuarioId: Mapped[uuid.UUID] = mapped_column(
        "usuario_id",
        UUID(as_uuid=True),
        ForeignKey("usuario.id", ondelete="SET NULL"),
        nullable=True,
    )
    criadoEm: Mapped[DateTime] = mapped_column(
        "criado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    estoque: Mapped["Estoque"] = relationship(
        "Estoque", back_populates="movimentacoes",
    )
    usuario: Mapped[Optional["Usuario"]] = relationship(
        "Usuario", back_populates="movimentacoesEstoque",
    )

    def __repr__(self) -> str:
        return f"<MovimentacaoEstoque tipo={self.tipo} quantidade={self.quantidade}>"