from sqlalchemy.orm import Session
from app.domain.models.estoque import Estoque, MovimentacaoEstoque
import uuid


def buscarPorUnidadeProduto(
    db: Session, unidadeId: uuid.UUID, produtoId: uuid.UUID
) -> Estoque | None:
    return (
        db.query(Estoque)
        .filter(
            Estoque.unidadeId == unidadeId,
            Estoque.produtoId == produtoId,
        )
        .first()
    )


def buscarPorUnidade(db: Session, unidadeId: uuid.UUID) -> list[Estoque]:
    return db.query(Estoque).filter(Estoque.unidadeId == unidadeId).all()


def criar(db: Session, estoque: Estoque) -> Estoque:
    db.add(estoque)
    db.commit()
    db.refresh(estoque)
    return estoque


def atualizar(db: Session, estoque: Estoque) -> Estoque:
    db.commit()
    db.refresh(estoque)
    return estoque


def registrarMovimentacao(
    db: Session, movimentacao: MovimentacaoEstoque
) -> MovimentacaoEstoque:
    db.add(movimentacao)
    db.commit()
    db.refresh(movimentacao)
    return movimentacao