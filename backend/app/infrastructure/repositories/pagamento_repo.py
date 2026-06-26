from sqlalchemy.orm import Session
from app.domain.models.pagamento import Pagamento
import uuid


def criar(db: Session, pagamento: Pagamento) -> Pagamento:
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)
    return pagamento


def buscarPorPedido(db: Session, pedidoId: uuid.UUID) -> Pagamento | None:
    return db.query(Pagamento).filter(Pagamento.pedidoId == pedidoId).first()


def buscarPorId(db: Session, pagamentoId: uuid.UUID) -> Pagamento | None:
    return db.query(Pagamento).filter(Pagamento.id == pagamentoId).first()


def atualizar(db: Session, pagamento: Pagamento) -> Pagamento:
    db.commit()
    db.refresh(pagamento)
    return pagamento