import uuid
from fastapi import APIRouter, HTTPException, status
from app.api.deps import DbDep, UsuarioAtualDep, requer_role
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.domain.models.produto import Produto
from app.domain.enums import RoleEnum

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=ProdutoResponse, status_code=201)
def criar(
    dados: ProdutoCreate,
    db: DbDep,
    admin=requer_role(RoleEnum.ADMIN, RoleEnum.GERENTE),
):
    produto = Produto(**dados.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


@router.get("", response_model=list[ProdutoResponse])
def listar(
    db: DbDep,
    _: UsuarioAtualDep,
    skip: int = 0,
    limit: int = 10,
):
    return db.query(Produto).filter(Produto.ativo == True).offset(skip).limit(limit).all()


@router.get("/{produtoId}", response_model=ProdutoResponse)
def buscar(produtoId: uuid.UUID, db: DbDep, _: UsuarioAtualDep):
    produto = db.query(Produto).filter(Produto.id == produtoId).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "PRODUTO_NAO_ENCONTRADO",
                "message": "Produto não encontrado.",
                "details": [],
            },
        )
    return produto


@router.patch("/{produtoId}", response_model=ProdutoResponse)
def atualizar(
    produtoId: uuid.UUID,
    dados: ProdutoUpdate,
    db: DbDep,
    admin=requer_role(RoleEnum.ADMIN, RoleEnum.GERENTE),
):
    produto = db.query(Produto).filter(Produto.id == produtoId).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "PRODUTO_NAO_ENCONTRADO",
                "message": "Produto não encontrado.",
                "details": [],
            },
        )
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto