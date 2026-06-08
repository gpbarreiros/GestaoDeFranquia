import uuid
from pydantic import BaseModel, field_validator
from datetime import datetime
from app.domain.enums import TipoMovimentacaoEstoqueEnum


class EstoqueResponse(BaseModel):
    id: uuid.UUID
    unidadeId: uuid.UUID
    produtoId: uuid.UUID
    quantidade: int
    atualizadoEm: datetime

    model_config = {"from_attributes": True}


class MovimentacaoEstoqueCreate(BaseModel):
    unidadeId: uuid.UUID
    produtoId: uuid.UUID
    tipo: TipoMovimentacaoEstoqueEnum
    quantidade: int
    motivo: str | None = None

    @field_validator("quantidade")
    @classmethod
    def quantidade_positiva(cls, v):
        if v < 1:
            raise ValueError("Quantidade deve ser maior que zero")
        return v


class MovimentacaoEstoqueResponse(BaseModel):
    id: uuid.UUID
    estoqueId: uuid.UUID
    tipo: TipoMovimentacaoEstoqueEnum
    quantidade: int
    motivo: str | None
    usuarioId: uuid.UUID | None
    criadoEm: datetime

    model_config = {"from_attributes": True}