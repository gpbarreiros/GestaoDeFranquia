import uuid
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from app.domain.enums import RoleEnum, BaseLegalEnum


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    role: RoleEnum
    baseLegalTratamento: BaseLegalEnum | None = None

    @field_validator("senha")
    @classmethod
    def validacao_senha(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        return value
    
    @field_validator("baseLegalTratamento")
    @classmethod
    def validacao_baseLegal(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("A base legal é obrigatoria, CONTRATO ou CONSENTIMENTO.")
        return value


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