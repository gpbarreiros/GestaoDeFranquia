import uuid
from fastapi import APIRouter, HTTPException, status
from app.api.deps import DbDep, UsuarioAtualDep, requer_role
from app.schemas.cardapio import (
    CardapioCreate, CardapioResponse, CardapioUpdate,
    CardapioItemCreate, CardapioItemResponse,
    CardapioPorUnidadeCreate, CardapioPorUnidadeResponse,
)
from app.domain.models.cardapio import Cardapio, CardapioItem, CardapioPorUnidade
from app.domain.enums import RoleEnum

router = APIRouter(prefix="/cardapios", tags=["Cardapios"])


@router.post("", response_model=CardapioResponse, status_code=201)
def criar(
    dados: CardapioCreate,
    db: DbDep,
    admin=requer_role(RoleEnum.ADMIN, RoleEnum.GERENTE),
):
    cardapio = Cardapio(**dados.model_dump())
    db.add(cardapio)
    db.commit()
    db.refresh(cardapio)
    return cardapio


@router.get("", response_model=list[CardapioResponse])
def listar(db: DbDep, _: UsuarioAtualDep, skip: int = 0, limit: int = 10):
    return db.query(Cardapio).offset(skip).limit(limit).all()


@router.get("/{cardapioId}", response_model=CardapioResponse)
def buscar(cardapioId: uuid.UUID, db: DbDep, _: UsuarioAtualDep):
    cardapio = db.query(Cardapio).filter(Cardapio.id == cardapioId).first()
    if not cardapio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "CARDAPIO_NAO_ENCONTRADO", "message": "Cardápio não encontrado.", "details": []},
        )
    return cardapio


@router.patch("/{cardapioId}", response_model=CardapioResponse)
def atualizar(
    cardapioId: uuid.UUID,
    dados: CardapioUpdate,
    db: DbDep,
    admin=requer_role(RoleEnum.ADMIN, RoleEnum.GERENTE),
):
    cardapio = db.query(Cardapio).filter(Cardapio.id == cardapioId).first()
    if not cardapio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "CARDAPIO_NAO_ENCONTRADO", "message": "Cardápio não encontrado.", "details": []},
        )
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(cardapio, campo, valor)
    db.commit()
    db.refresh(cardapio)
    return cardapio


@router.post("/{cardapioId}/itens", response_model=CardapioItemResponse, status_code=201)
def adicionarItem(
    cardapioId: uuid.UUID,
    dados: CardapioItemCreate,
    db: DbDep,
    admin=requer_role(RoleEnum.ADMIN, RoleEnum.GERENTE),
):
    item = CardapioItem(cardapioId=cardapioId, **dados.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{cardapioId}/itens", response_model=list[CardapioItemResponse])
def listarItens(cardapioId: uuid.UUID, db: DbDep, _: UsuarioAtualDep):
    return db.query(CardapioItem).filter(CardapioItem.cardapioId == cardapioId).all()


@router.post("/{cardapioId}/unidades", response_model=CardapioPorUnidadeResponse, status_code=201)
def vincularUnidade(
    cardapioId: uuid.UUID,
    dados: CardapioPorUnidadeCreate,
    db: DbDep,
    admin=requer_role(RoleEnum.ADMIN, RoleEnum.GERENTE),
):
    vinculo = CardapioPorUnidade(cardapioId=cardapioId, **dados.model_dump())
    db.add(vinculo)
    db.commit()
    db.refresh(vinculo)
    return vinculo


@router.get("/{cardapioId}/unidades", response_model=list[CardapioPorUnidadeResponse])
def listarUnidades(cardapioId: uuid.UUID, db: DbDep, _: UsuarioAtualDep):
    return db.query(CardapioPorUnidade).filter(CardapioPorUnidade.cardapioId == cardapioId).all()