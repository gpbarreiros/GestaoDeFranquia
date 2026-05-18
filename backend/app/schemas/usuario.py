import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.domain.enums import RoleEnum, BaseLegalEnum


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    role: RoleEnum
    baseLegalTratamento: BaseLegalEnum


class UsuarioResponse(BaseModel):
    id: uuid.UUID
    nome: str
    email: EmailStr
    role: RoleEnum
    ativo: bool
    criadoEm: datetime

    model_config = {"from_attributes": True}


class UsuarioUpdate(BaseModel):
    nome: str | None = None
    ativo: bool | None = None