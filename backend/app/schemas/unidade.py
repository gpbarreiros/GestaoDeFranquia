import uuid
from pydantic import BaseModel
from datetime import datetime


class UnidadeCreate(BaseModel):
    nome: str
    endereco: str | None = None
    cidade: str | None = None


class UnidadeResponse(BaseModel):
    id: uuid.UUID
    nome: str
    endereco: str | None
    cidade: str | None
    ativa: bool
    criadoEm: datetime

    model_config = {"from_attributes": True}


class UnidadeUpdate(BaseModel):
    nome: str | None = None
    endereco: str | None = None
    cidade: str | None = None
    ativa: bool | None = None