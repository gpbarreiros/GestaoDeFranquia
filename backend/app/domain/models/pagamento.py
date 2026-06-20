import uuid
from typing import Optional
from sqlalchemy import DateTime, Numeric, ForeignKey, func, UniqueConstraint, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.infrastructure.database import Base
from app.domain.enums import FormaPagamentoEnum, StatusPagamentoEnum


class Pagamento(Base):
    __tablename__ = "pagamento"
    __table_args__ = (
        UniqueConstraint("pedido_id", name="uq_pagamento_pedido"),
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
    forma: Mapped[FormaPagamentoEnum] = mapped_column(
        SAEnum(FormaPagamentoEnum, name="forma_pagamento_enum"),
        nullable=False,
    )
    status: Mapped[StatusPagamentoEnum] = mapped_column(
        SAEnum(StatusPagamentoEnum, name="status_pagamento_enum"),
        default=StatusPagamentoEnum.PENDENTE,
        nullable=False,
    )
    valor: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    gatewayId: Mapped[Optional[str]] = mapped_column(
        "gateway_id",
        UUID(as_uuid=True),
        nullable=True,
    )
    gatewayPayload: Mapped[Optional[dict]] = mapped_column(
        "gateway_payload",
        JSONB,
        nullable=True,
    )
    processadoEm: Mapped[Optional[DateTime]] = mapped_column(
        "processado_em",
        DateTime(timezone=True),
        nullable=True,
    )
    criadoEm: Mapped[DateTime] = mapped_column(
        "criado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    pedido: Mapped["Pedido"] = relationship(
        "Pedido", back_populates="pagamento",
    )

    def __repr__(self) -> str:
        return f"<Pagamento id={self.id} status={self.status} valor={self.valor}>"