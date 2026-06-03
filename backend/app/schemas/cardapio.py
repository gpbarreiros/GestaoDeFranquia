import uuid
from pydantic import BaseModel
from datetime import datetime, date


class CardapioCreate(BaseModel):
    nome: str
    descricao: str | None = None
    periodoInicio: date | None = None
    periodoFim: date | None = None


class CardapioResponse(BaseModel):
    id: uuid.UUID
    nome: str
    descricao: str | None
    periodoInicio: date | None
    periodoFim: date | None
    ativo: bool
    criadoEm: datetime

    model_config = {"from_attributes": True}


class CardapioUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    periodoInicio: date | None = None
    periodoFim: date | None = None
    ativo: bool | None = None


class CardapioItemCreate(BaseModel):
    produtoId: uuid.UUID
    disponivel: bool = True


class CardapioItemResponse(BaseModel):
    id: uuid.UUID
    cardapioId: uuid.UUID
    produtoId: uuid.UUID
    disponivel: bool

    model_config = {"from_attributes": True}


class CardapioPorUnidadeCreate(BaseModel):
    unidadeId: uuid.UUID
    ativo: bool = True


class CardapioPorUnidadeResponse(BaseModel):
    id: uuid.UUID
    cardapioId: uuid.UUID
    unidadeId: uuid.UUID
    ativo: bool

    model_config = {"from_attributes": True}