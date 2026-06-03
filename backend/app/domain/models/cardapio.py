import uuid
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Date, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base


class Cardapio(Base):
    __tablename__ = "cardapio"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    periodoInicio: Mapped[Optional[Date]] = mapped_column(
        "periodo_inicio", Date, nullable=True,
    )
    periodoFim: Mapped[Optional[Date]] = mapped_column(
        "periodo_fim", Date, nullable=True,
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criadoEm: Mapped[DateTime] = mapped_column(
        "criado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    itens: Mapped[list["CardapioItem"]] = relationship(
        "CardapioItem",
        back_populates="cardapio",
        cascade="all, delete-orphan",
    )
    unidades: Mapped[list["CardapioPorUnidade"]] = relationship(
        "CardapioPorUnidade",
        back_populates="cardapio",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Cardapio id={self.id} nome={self.nome}>"


class CardapioItem(Base):
    __tablename__ = "cardapio_item"
    __table_args__ = (
        UniqueConstraint("cardapio_id", "produto_id", name="uq_cardapio_item"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    cardapioId: Mapped[uuid.UUID] = mapped_column(
        "cardapio_id",
        UUID(as_uuid=True),
        ForeignKey("cardapio.id", ondelete="CASCADE"),
        nullable=False,
    )
    produtoId: Mapped[uuid.UUID] = mapped_column(
        "produto_id",
        UUID(as_uuid=True),
        ForeignKey("produto.id", ondelete="CASCADE"),
        nullable=False,
    )
    disponivel: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cardapio: Mapped["Cardapio"] = relationship(
        "Cardapio", back_populates="itens",
    )
    produto: Mapped["Produto"] = relationship(
        "Produto", back_populates="cardapioItens",
    )

    def __repr__(self) -> str:
        return f"<CardapioItem cardapioId={self.cardapioId} produtoId={self.produtoId}>"


class CardapioPorUnidade(Base):
    __tablename__ = "cardapio_por_unidade"
    __table_args__ = (
        UniqueConstraint("cardapio_id", "unidade_id", name="uq_cardapio_unidade"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    cardapioId: Mapped[uuid.UUID] = mapped_column(
        "cardapio_id",
        UUID(as_uuid=True),
        ForeignKey("cardapio.id", ondelete="CASCADE"),
        nullable=False,
    )
    unidadeId: Mapped[uuid.UUID] = mapped_column(
        "unidade_id",
        UUID(as_uuid=True),
        ForeignKey("unidade.id", ondelete="CASCADE"),
        nullable=False,
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cardapio: Mapped["Cardapio"] = relationship(
        "Cardapio", back_populates="unidades",
    )
    unidade: Mapped["Unidade"] = relationship(
        "Unidade", back_populates="cardapiosPorUnidade",
    )

    def __repr__(self) -> str:
        return f"<CardapioPorUnidade cardapioId={self.cardapioId} unidadeId={self.unidadeId}>"