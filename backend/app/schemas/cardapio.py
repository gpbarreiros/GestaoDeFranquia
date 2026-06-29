import uuid
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal


class CardapioCreate(BaseModel):
    nome: str
    descricao: str | None = None
    periodoInicio: date | None = None
    periodoFim: date | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "nome": "Cardápio Padrão",
                "descricao": "Cardápio principal da rede",
                "periodoInicio": None,
                "periodoFim": None,
            }
        }
    }


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

    model_config = {
        "json_schema_extra": {
            "example": {
                "produtoId": "fc9caa99-4321-4e88-9eb3-658e654d22b1",
                "disponivel": True,
            }
        }
    }


class CardapioItemResponse(BaseModel):
    id: uuid.UUID
    cardapioId: uuid.UUID
    produtoId: uuid.UUID
    disponivel: bool
    nomeProduto: str | None = None
    descricaoProduto: str | None = None
    precoProduto: Decimal | None = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "uuid-do-item",
                "cardapioId": "uuid-do-cardapio",
                "produtoId": "uuid-do-produto",
                "disponivel": True,
                "nomeProduto": "X-Burguer Nordestino",
                "descricaoProduto": "Hambúrguer artesanal com coalho",
                "precoProduto": 29.90,
            }
        }
    }


class CardapioPorUnidadeCreate(BaseModel):
    unidadeId: uuid.UUID
    ativo: bool = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "unidadeId": "uuid-da-unidade",
                "ativo": True,
            }
        }
    }


class CardapioPorUnidadeResponse(BaseModel):
    id: uuid.UUID
    cardapioId: uuid.UUID
    unidadeId: uuid.UUID
    ativo: bool
    nomeCardapio: str | None = None
    periodoInicio: date | None = None
    periodoFim: date | None = None
    nomeUnidade: str | None = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "uuid-do-vinculo",
                "cardapioId": "uuid-do-cardapio",
                "unidadeId": "uuid-da-unidade",
                "ativo": True,
                "nomeCardapio": "Cardápio Padrão",
                "periodoInicio": None,
                "periodoFim": None,
                "nomeUnidade": "Unidade Centro Recife",
            }
        }
    }