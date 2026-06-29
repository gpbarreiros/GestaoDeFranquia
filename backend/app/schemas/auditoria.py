import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class LogAuditoriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    usuarioId: Optional[uuid.UUID] = None
    acao: str
    entidade: str
    entidadeId: Optional[str] = None
    detalhe: Optional[dict[str, Any]] = None
    ipOrigem: Optional[str] = None
    criadoEm: datetime
