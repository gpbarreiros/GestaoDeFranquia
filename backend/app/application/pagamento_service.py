from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.models.pagamento import Pagamento
from app.domain.models.usuario import LogAuditoria
from app.domain.enums import StatusPagamentoEnum, StatusPedidoEnum
from app.infrastructure.repositories import pagamento_repo, pedido_repo, usuario_repo
from app.infrastructure.gateway.pagamento_mock import processarPagamento
from app.application import fidelidade_service


def processar(
    db: Session,
    pedidoId,
    forma,
    usuarioAtual,
    ipOrigem: str | None = None,
) -> Pagamento:
    pedido = pedido_repo.buscarPorId(db, pedidoId)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "PEDIDO_NAO_ENCONTRADO",
                "message": "Pedido não encontrado.",
                "details": [],
            },
        )

    if pedido.status != StatusPedidoEnum.AGUARDANDO_PAGAMENTO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "PEDIDO_STATUS_INVALIDO",
                "message": f"Pedido não está aguardando pagamento. Status atual: {pedido.status.value}",
                "details": [],
            },
        )

    pagamentoExistente = pagamento_repo.buscarPorPedido(db, pedidoId)
    if pagamentoExistente and pagamentoExistente.status == StatusPagamentoEnum.APROVADO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "PAGAMENTO_JA_APROVADO",
                "message": "Este pedido já possui um pagamento aprovado.",
                "details": [],
            },
        )

    resultado = processarPagamento(pedidoId, float(pedido.total), forma.value)

    pagamento = Pagamento(
        pedidoId=pedidoId,
        forma=forma,
        status=StatusPagamentoEnum.APROVADO if resultado["aprovado"] else StatusPagamentoEnum.RECUSADO,
        valor=pedido.total,
        gatewayId=resultado["gatewayId"],
        gatewayPayload=resultado,
        processadoEm=datetime.now(timezone.utc),
    )
    pagamento_repo.criar(db, pagamento)

    if resultado["aprovado"]:
        pedido.status = StatusPedidoEnum.PAGO
        pedido_repo.atualizar(db, pedido)
        fidelidade_service.creditarPontos(db, pedido.clienteId, pedido.id, float(pedido.total))

    log = LogAuditoria(
        usuarioId=usuarioAtual.id,
        acao="PROCESSAR_PAGAMENTO",
        entidade="pagamento",
        entidadeId=str(pagamento.id),
        detalhe={
            "pedidoId": str(pedidoId),
            "valor": float(pedido.total),
            "status": pagamento.status.value,
            "aprovado": resultado["aprovado"],
        },
        ipOrigem=ipOrigem,
    )
    usuario_repo.registrarLog(db, log)

    return pagamento