import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.models.fidelidade import Fidelidade, MovimentacaoFidelidade
from app.domain.enums import TipoMovimentacaoFidelidadeEnum
from app.schemas.fidelidade import ResgateRequest


def creditarPontos(
    db: Session,
    clienteId: uuid.UUID,
    pedidoId: uuid.UUID,
    total: float,
) -> Fidelidade:
    pontos = int(total)

    fidelidade = db.query(Fidelidade).filter(
        Fidelidade.clienteId == clienteId
    ).first()

    if not fidelidade:
        fidelidade = Fidelidade(clienteId=clienteId, pontosSaldo=0)
        db.add(fidelidade)
        db.flush()

    fidelidade.pontosSaldo += pontos

    movimentacao = MovimentacaoFidelidade(
        fidelidadeId=fidelidade.id,
        pedidoId=pedidoId,
        tipo=TipoMovimentacaoFidelidadeEnum.CREDITO,
        pontos=pontos,
        descricao=f"Crédito por pedido #{pedidoId}",
    )
    db.add(movimentacao)
    db.commit()
    db.refresh(fidelidade)
    return fidelidade


def resgatar(
    db: Session,
    clienteId: uuid.UUID,
    dados: ResgateRequest,
) -> Fidelidade:
    fidelidade = db.query(Fidelidade).filter(
        Fidelidade.clienteId == clienteId
    ).first()

    if not fidelidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "FIDELIDADE_NAO_ENCONTRADA",
                "message": "Programa de fidelidade não encontrado para este cliente.",
                "details": [],
            },
        )

    if fidelidade.pontosSaldo < dados.pontos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "PONTOS_INSUFICIENTES",
                "message": "Saldo de pontos insuficiente.",
                "details": [
                    {
                        "field": "pontos",
                        "issue": f"Disponível: {fidelidade.pontosSaldo}",
                    }
                ],
            },
        )

    fidelidade.pontosSaldo -= dados.pontos

    movimentacao = MovimentacaoFidelidade(
        fidelidadeId=fidelidade.id,
        pedidoId=None,
        tipo=TipoMovimentacaoFidelidadeEnum.DEBITO,
        pontos=dados.pontos,
        descricao=dados.descricao or "Resgate de pontos",
    )
    db.add(movimentacao)
    db.commit()
    db.refresh(fidelidade)
    return fidelidade


def consultarSaldo(db: Session, clienteId: uuid.UUID) -> Fidelidade:
    fidelidade = db.query(Fidelidade).filter(
        Fidelidade.clienteId == clienteId
    ).first()

    if not fidelidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "FIDELIDADE_NAO_ENCONTRADA",
                "message": "Programa de fidelidade não encontrado.",
                "details": [],
            },
        )
    return fidelidade