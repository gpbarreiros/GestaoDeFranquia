import uuid
from fastapi import APIRouter
from app.api.deps import DbDep, UsuarioAtualDep, requer_role
from app.schemas.unidade import UnidadeCreate, UnidadeResponse, UnidadeUpdate
from app.domain.models.unidade import Unidade
from app.domain.enums import RoleEnum
from fastapi import HTTPException, status

router = APIRouter(prefix="/unidades", tags=["Unidades"])


@router.post("", response_model=UnidadeResponse, status_code=201)
def criar(
    dados: UnidadeCreate,
    db: DbDep,
    admin=requer_role(RoleEnum.ADMIN),
):
    unidade = Unidade(**dados.model_dump())
    db.add(unidade)
    db.commit()
    db.refresh(unidade)
    return unidade


@router.get("", response_model=list[UnidadeResponse])
def listar(db: DbDep, _: UsuarioAtualDep, skip: int = 0, limit: int = 10):
    return db.query(Unidade).offset(skip).limit(limit).all()


@router.get("/{unidadeId}", response_model=UnidadeResponse)
def buscar(unidadeId: uuid.UUID, db: DbDep, _: UsuarioAtualDep):
    unidade = db.query(Unidade).filter(Unidade.id == unidadeId).first()
    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "UNIDADE_NAO_ENCONTRADA",
                "message": "Unidade não encontrada.",
                "details": [],
            },
        )
    return unidade


@router.patch("/{unidadeId}", response_model=UnidadeResponse)
def atualizar(
    unidadeId: uuid.UUID,
    dados: UnidadeUpdate,
    db: DbDep,
    admin=requer_role(RoleEnum.ADMIN, RoleEnum.GERENTE),
):
    unidade = db.query(Unidade).filter(Unidade.id == unidadeId).first()
    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "UNIDADE_NAO_ENCONTRADA",
                "message": "Unidade não encontrada.",
                "details": [],
            },
        )
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(unidade, campo, valor)
    db.commit()
    db.refresh(unidade)
    return unidade