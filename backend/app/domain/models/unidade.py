import uuid
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base


class Unidade(Base):
    __tablename__ = "unidade"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    cidade: Mapped[str] = mapped_column(String(100), nullable=True)
    ativa: Mapped[bool] = mapped_column(
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
    pedidos: Mapped[list["Pedido"]] = relationship(
        "Pedido",
        back_populates="unidade",
    )
    estoques: Mapped[list["Estoque"]] = relationship(
        "Estoque",
        back_populates="unidade",
        cascade="all, delete-orphan",
    )
    cardapiosPorUnidade: Mapped[list["CardapioPorUnidade"]] = relationship(
        "CardapioPorUnidade",
        back_populates="unidade",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Unidade id={self.id} nome={self.nome}>"