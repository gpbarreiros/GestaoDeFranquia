import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.models.estoque import Estoque, MovimentacaoEstoque
from app.domain.models.usuario import LogAuditoria
from app.domain.enums import TipoMovimentacaoEstoqueEnum
from app.infrastructure.repositories import estoque_repo, usuario_repo
from app.schemas.estoque import MovimentacaoEstoqueCreate


def movimentar(
    db: Session,
    dados: MovimentacaoEstoqueCreate,
    usuarioAtual,
    ipOrigem: str | None = None,
) -> Estoque:
    estoque = estoque_repo.buscarPorUnidadeProduto(
        db, dados.unidadeId, dados.produtoId
    )

    if not estoque:
        if dados.tipo == TipoMovimentacaoEstoqueEnum.SAIDA:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "ESTOQUE_NAO_ENCONTRADO",
                    "message": "Estoque não encontrado para este produto nesta unidade.",
                    "details": [],
                },
            )
        estoque = Estoque(
            unidadeId=dados.unidadeId,
            produtoId=dados.produtoId,
            quantidade=0,
        )
        estoque_repo.criar(db, estoque)

    if dados.tipo == TipoMovimentacaoEstoqueEnum.SAIDA:
        if estoque.quantidade < dados.quantidade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "ESTOQUE_INSUFICIENTE",
                    "message": "Quantidade insuficiente em estoque.",
                    "details": [
                        {
                            "field": "quantidade",
                            "issue": f"Disponível: {estoque.quantidade}",
                        }
                    ],
                },
            )
        estoque.quantidade -= dados.quantidade
    elif dados.tipo == TipoMovimentacaoEstoqueEnum.ENTRADA:
        estoque.quantidade += dados.quantidade
    else:
        estoque.quantidade = dados.quantidade

    estoque_repo.atualizar(db, estoque)

    movimentacao = MovimentacaoEstoque(
        estoqueId=estoque.id,
        tipo=dados.tipo,
        quantidade=dados.quantidade,
        motivo=dados.motivo,
        usuarioId=usuarioAtual.id,
    )
    estoque_repo.registrarMovimentacao(db, movimentacao)

    log = LogAuditoria(
        usuarioId=usuarioAtual.id,
        acao="MOVIMENTAR_ESTOQUE",
        entidade="estoque",
        entidadeId=str(estoque.id),
        detalhe={
            "tipo": dados.tipo.value,
            "quantidade": dados.quantidade,
            "motivo": dados.motivo,
        },
        ipOrigem=ipOrigem,
    )
    usuario_repo.registrarLog(db, log)

    return estoque


def consultarPorUnidade(db: Session, unidadeId: uuid.UUID) -> list[Estoque]:
    return estoque_repo.buscarPorUnidade(db, unidadeId)