from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Query
from app.api.deps import DbDep, requer_role
from app.domain.models.usuario import LogAuditoria
from app.domain.enums import RoleEnum
from app.schemas.auditoria import LogAuditoriaResponse

router = APIRouter(prefix="/auditoria", tags=["Auditoria"])


@router.get("", response_model=list[LogAuditoriaResponse])
def listarLogs(
    db: DbDep,
    admin=requer_role(RoleEnum.ADMIN),
    entidade: Optional[str] = Query(None, description="Filtrar por entidade (ex: pedido, pagamento, usuario)"),
    acao: Optional[str] = Query(None, description="Filtrar por ação (ex: CRIAR_PEDIDO, PROCESSAR_PAGAMENTO)"),
    dataInicio: Optional[datetime] = Query(None, description="Data inicial (ISO 8601)"),
    dataFim: Optional[datetime] = Query(None, description="Data final (ISO 8601)"),
    skip: int = 0,
    limit: int = 50,
):
    query = db.query(LogAuditoria)

    if entidade:
        query = query.filter(LogAuditoria.entidade == entidade)
    if acao:
        query = query.filter(LogAuditoria.acao == acao)
    if dataInicio:
        query = query.filter(LogAuditoria.criadoEm >= dataInicio)
    if dataFim:
        query = query.filter(LogAuditoria.criadoEm <= dataFim)

    return (
        query.order_by(LogAuditoria.criadoEm.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
