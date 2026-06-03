import uuid
from sqlalchemy import String, Boolean, DateTime, Numeric, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base


class Produto(Base):
    __tablename__ = "produto"
    __table_args__ = (
        CheckConstraint("preco >= 0", name="ck_produto_preco_positivo"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=True)
    preco: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    criadoEm: Mapped[DateTime] = mapped_column(
        "criado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relacionamentos
    cardapioItens: Mapped[list["CardapioItem"]] = relationship(
        "CardapioItem",
        back_populates="produto",
    )
    estoques: Mapped[list["Estoque"]] = relationship(
        "Estoque",
        back_populates="produto",
    )
    itensPedido: Mapped[list["ItemPedido"]] = relationship(
        "ItemPedido",
        back_populates="produto",
    )

    def __repr__(self) -> str:
        return f"<Produto id={self.id} nome={self.nome} preco={self.preco}>"