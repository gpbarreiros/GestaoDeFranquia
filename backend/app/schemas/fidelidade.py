import uuid
from pydantic import BaseModel
from datetime import datetime
from app.domain.enums import TipoMovimentacaoFidelidadeEnum


class FidelidadeResponse(BaseModel):
    id: uuid.UUID
    clienteId: uuid.UUID
    pontosSaldo: int
    atualizadoEm: datetime

    model_config = {"from_attributes": True}


class MovimentacaoFidelidadeResponse(BaseModel):
    id: uuid.UUID
    fidelidadeId: uuid.UUID
    pedidoId: uuid.UUID | None
    tipo: TipoMovimentacaoFidelidadeEnum
    pontos: int
    descricao: str | None
    criadoEm: datetime

    model_config = {"from_attributes": True}


class ResgateRequest(BaseModel):
    pontos: int
    descricao: str | None = None