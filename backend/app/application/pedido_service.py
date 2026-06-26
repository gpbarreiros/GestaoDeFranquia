import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.models.pedido import Pedido, ItemPedido
from app.domain.models.usuario import LogAuditoria
from app.domain.enums import StatusPedidoEnum, TRANSICOES_STATUS_PEDIDO
from app.infrastructure.repositories import pedido_repo, estoque_repo, usuario_repo
from app.schemas.pedido import PedidoCreate, PedidoStatusUpdate
from app.domain.models.produto import Produto


def criar(
    db: Session,
    dados: PedidoCreate,
    usuarioAtual,
    ipOrigem: str | None = None,
) -> Pedido:
    itensProcessados = []
    total = 0

    for item in dados.itens:
        produto = db.query(Produto).filter(
            Produto.id == item.produtoId,
            Produto.ativo == True,
        ).first()

        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "PRODUTO_NAO_ENCONTRADO",
                    "message": f"Produto {item.produtoId} não encontrado ou inativo.",
                    "details": [{"field": "produtoId", "issue": str(item.produtoId)}],
                },
            )

        estoque = estoque_repo.buscarPorUnidadeProduto(
            db, dados.unidadeId, item.produtoId
        )

        if not estoque or estoque.quantidade < item.quantidade:
            disponivel = estoque.quantidade if estoque else 0
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "ESTOQUE_INSUFICIENTE",
                    "message": f"Estoque insuficiente para o produto {produto.nome}.",
                    "details": [
                        {
                            "field": f"itens[produtoId={item.produtoId}].quantidade",
                            "issue": f"Disponível: {disponivel}",
                        }
                    ],
                },
            )

        subtotal = float(produto.preco) * item.quantidade
        total += subtotal
        itensProcessados.append((produto, item.quantidade, subtotal))

    pedido = Pedido(
        clienteId=usuarioAtual.id,
        unidadeId=dados.unidadeId,
        canalPedido=dados.canalPedido,
        status=StatusPedidoEnum.AGUARDANDO_PAGAMENTO,
        total=total,
        observacao=dados.observacao,
    )
    db.add(pedido)
    db.flush()

    for produto, quantidade, subtotal in itensProcessados:
        itemPedido = ItemPedido(
            pedidoId=pedido.id,
            produtoId=produto.id,
            quantidade=quantidade,
            precoUnitario=produto.preco,
            subtotal=subtotal,
        )
        db.add(itemPedido)

        estoque = estoque_repo.buscarPorUnidadeProduto(
            db, dados.unidadeId, produto.id
        )
        estoque.quantidade -= quantidade

    db.commit()
    db.refresh(pedido)

    log = LogAuditoria(
        usuarioId=usuarioAtual.id,
        acao="CRIAR_PEDIDO",
        entidade="pedido",
        entidadeId=str(pedido.id),
        detalhe={
            "unidadeId": str(dados.unidadeId),
            "canalPedido": dados.canalPedido.value,
            "total": total,
            "itens": len(dados.itens),
        },
        ipOrigem=ipOrigem,
    )
    usuario_repo.registrarLog(db, log)

    return pedido


def atualizarStatus(
    db: Session,
    pedidoId: uuid.UUID,
    dados: PedidoStatusUpdate,
    usuarioAtual,
    ipOrigem: str | None = None,
) -> Pedido:
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

    transicoesPermitidas = TRANSICOES_STATUS_PEDIDO.get(pedido.status, [])
    if dados.status not in transicoesPermitidas:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "TRANSICAO_STATUS_INVALIDA",
                "message": f"Não é possível mudar de {pedido.status.value} para {dados.status.value}.",
                "details": [
                    {
                        "field": "status",
                        "issue": f"Transições permitidas: {[s.value for s in transicoesPermitidas]}",
                    }
                ],
            },
        )

    statusAnterior = pedido.status.value
    pedido.status = dados.status
    pedido_repo.atualizar(db, pedido)

    log = LogAuditoria(
        usuarioId=usuarioAtual.id,
        acao="ATUALIZAR_STATUS_PEDIDO",
        entidade="pedido",
        entidadeId=str(pedido.id),
        detalhe={
            "statusAnterior": statusAnterior,
            "statusNovo": dados.status.value,
        },
        ipOrigem=ipOrigem,
    )
    usuario_repo.registrarLog(db, log)

    return pedido


def listar(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    status: StatusPedidoEnum | None = None,
    canalPedido=None,
    clienteId: uuid.UUID | None = None,
    unidadeId: uuid.UUID | None = None,
) -> list[Pedido]:
    return pedido_repo.listar(
        db,
        skip=skip,
        limit=limit,
        status=status,
        canalPedido=canalPedido,
        clienteId=clienteId,
        unidadeId=unidadeId,
    )


def buscarPorId(db: Session, pedidoId: uuid.UUID) -> Pedido:
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
    return pedido