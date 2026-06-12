import uuid
from pydantic import BaseModel, field_validator
from datetime import datetime
from decimal import Decimal
from app.domain.enums import CanalPedidoEnum, StatusPedidoEnum


class ItemPedidoCreate(BaseModel):
    produtoId: uuid.UUID
    quantidade: int

    @field_validator("quantidade")
    @classmethod
    def quantidade_positiva(cls, v):
        if v < 1:
            raise ValueError("Quantidade deve ser maior que zero")
        return v


class ItemPedidoResponse(BaseModel):
    id: uuid.UUID
    produtoId: uuid.UUID
    quantidade: int
    precoUnitario: Decimal
    subtotal: Decimal

    model_config = {"from_attributes": True}


class PedidoCreate(BaseModel):
    unidadeId: uuid.UUID
    canalPedido: CanalPedidoEnum
    itens: list[ItemPedidoCreate]
    observacao: str | None = None

    @field_validator("itens")
    @classmethod
    def itens_nao_vazios(cls, v):
        if not v:
            raise ValueError("Pedido deve ter ao menos um item")
        return v


class PedidoResponse(BaseModel):
    id: uuid.UUID
    clienteId: uuid.UUID
    unidadeId: uuid.UUID
    canalPedido: CanalPedidoEnum
    status: StatusPedidoEnum
    total: Decimal
    observacao: str | None
    itens: list[ItemPedidoResponse]
    criadoEm: datetime
    atualizadoEm: datetime

    model_config = {"from_attributes": True}


class PedidoStatusUpdate(BaseModel):
    status: StatusPedidoEnum