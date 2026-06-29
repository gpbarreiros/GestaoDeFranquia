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


@router.get("/{cardapioId}/itens", response_model=list[CardapioItemResponse])
def listarItens(cardapioId: uuid.UUID, db: DbDep, _: UsuarioAtualDep):
    from app.domain.models.produto import Produto
    itens = db.query(CardapioItem).filter(
        CardapioItem.cardapioId == cardapioId
    ).all()
    
    resultado = []
    for item in itens:
        produto = db.query(Produto).filter(Produto.id == item.produtoId).first()
        itemDict = {
            "id": item.id,
            "cardapioId": item.cardapioId,
            "produtoId": item.produtoId,
            "disponivel": item.disponivel,
            "nomeProduto": produto.nome if produto else None,
            "descricaoProduto": produto.descricao if produto else None,
            "precoProduto": produto.preco if produto else None,
        }
        resultado.append(itemDict)
    
    return resultado


@router.get("/{cardapioId}/itens", response_model=list[CardapioItemResponse])
def listarItens(cardapioId: uuid.UUID, db: DbDep, _: UsuarioAtualDep):
    from app.domain.models.produto import Produto

    cardapio = db.query(Cardapio).filter(Cardapio.id == cardapioId).first()
    if not cardapio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "CARDAPIO_NAO_ENCONTRADO",
                "message": "Cardápio não encontrado.",
                "details": [],
            },
        )

    if not cardapio.ativo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "CARDAPIO_INATIVO",
                "message": "Este cardápio está inativo e não pode ser consultado.",
                "details": [
                    {
                        "field": "ativo",
                        "issue": "Cardápio inativo",
                    }
                ],
            },
        )

    itens = db.query(CardapioItem).filter(
        CardapioItem.cardapioId == cardapioId
    ).all()

    resultado = []
    for item in itens:
        produto = db.query(Produto).filter(Produto.id == item.produtoId).first()
        itemDict = {
            "id": item.id,
            "cardapioId": item.cardapioId,
            "produtoId": item.produtoId,
            "disponivel": item.disponivel,
            "nomeProduto": produto.nome if produto else None,
            "descricaoProduto": produto.descricao if produto else None,
            "precoProduto": produto.preco if produto else None,
        }
        resultado.append(itemDict)

    return resultado


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
    from app.domain.models.unidade import Unidade
    vinculos = db.query(CardapioPorUnidade).filter(
        CardapioPorUnidade.cardapioId == cardapioId
    ).all()

    resultado = []
    for vinculo in vinculos:
        cardapio = db.query(Cardapio).filter(Cardapio.id == vinculo.cardapioId).first()
        unidade = db.query(Unidade).filter(Unidade.id == vinculo.unidadeId).first()
        resultado.append({
            "id": vinculo.id,
            "cardapioId": vinculo.cardapioId,
            "unidadeId": vinculo.unidadeId,
            "ativo": vinculo.ativo,
            "nomeCardapio": cardapio.nome if cardapio else None,
            "periodoInicio": cardapio.periodoInicio if cardapio else None,
            "periodoFim": cardapio.periodoFim if cardapio else None,
            "nomeUnidade": unidade.nome if unidade else None,
        })

    return resultado