import uuid
from pydantic import BaseModel, field_validator
from datetime import datetime
from decimal import Decimal


class ProdutoCreate(BaseModel):
    nome: str
    descricao: str | None = None
    preco: Decimal

    @field_validator("preco")
    @classmethod
    def preco_positivo(cls, v):
        if v < 0:
            raise ValueError("Preço não pode ser negativo")
        return v


class ProdutoResponse(BaseModel):
    id: uuid.UUID
    nome: str
    descricao: str | None
    preco: Decimal
    ativo: bool
    criadoEm: datetime

    model_config = {"from_attributes": True}


class ProdutoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    preco: Decimal | None = None
    ativo: bool | None = None