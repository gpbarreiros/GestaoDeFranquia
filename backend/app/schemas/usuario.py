import uuid
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from app.domain.enums import RoleEnum, BaseLegalEnum


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str  | None = None
    role: RoleEnum
    baseLegalTratamento: BaseLegalEnum 
    @field_validator("senha")
    @classmethod
    def validacao_senha(cls, value: str) -> str:
        if len(value) < 8 or value is None or value.strip() == "":
            raise ValueError("A senha é obrigatória e deve ter pelo menos 8 caracteres.")
        return value
    
    @field_validator("baseLegalTratamento", mode="before")
    @classmethod
    def validacao_baseLegal(cls, value: BaseLegalEnum) -> BaseLegalEnum:
        if value not in [BaseLegalEnum.CONTRATO, BaseLegalEnum.CONSENTIMENTO]:
            raise ValueError("A base legal de tratamento é obrigatória. CONTRATO ou CONSENTIMENTO.")
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