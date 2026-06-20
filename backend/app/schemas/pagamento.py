import uuid
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from app.domain.enums import FormaPagamentoEnum, StatusPagamentoEnum


class PagamentoCreate(BaseModel):
    pedidoId: uuid.UUID
    forma: FormaPagamentoEnum = FormaPagamentoEnum.MOCK


class PagamentoResponse(BaseModel):
    id: uuid.UUID
    pedidoId: uuid.UUID
    forma: FormaPagamentoEnum
    status: StatusPagamentoEnum
    valor: Decimal
    gatewayId: uuid.UUID | None
    gatewayPayload: dict | None
    processadoEm: datetime | None
    criadoEm: datetime

    model_config = {"from_attributes": True}