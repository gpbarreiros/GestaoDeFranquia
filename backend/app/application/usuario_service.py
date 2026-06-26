import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.models.usuario import Usuario, ConsentimentoLgpd, LogAuditoria
from app.domain.enums import RoleEnum, BaseLegalEnum
from app.infrastructure.repositories import usuario_repo
from app.core.security import hashSenha
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


def criar(db: Session, dados: UsuarioCreate, ipOrigem: str | None = None) -> Usuario:
    existente = usuario_repo.buscarPorEmail(db, dados.email)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "EMAIL_JA_CADASTRADO",
                "message": "Já existe um usuário com este e-mail.",
                "details": [{"field": "email", "issue": "email já cadastrado"}],
            },
        )

    baseLegal = (
        BaseLegalEnum.CONSENTIMENTO
        if dados.role == RoleEnum.CLIENTE
        else BaseLegalEnum.CONTRATO
    )

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senhaHash=hashSenha(dados.senha),
        role=dados.role,
        baseLegalTratamento=baseLegal,
    )
    usuario_repo.criar(db, usuario)

    if dados.role == RoleEnum.CLIENTE:
        consentimento = ConsentimentoLgpd(
            usuarioId=usuario.id,
            finalidade="Cadastro e uso da plataforma Gestão de Franquias",
            aceito=True,
        )
        usuario_repo.criarConsentimento(db, consentimento)

    log = LogAuditoria(
        usuarioId=usuario.id,
        acao="CRIAR_USUARIO",
        entidade="usuario",
        entidadeId=str(usuario.id),
        detalhe={"email": usuario.email, "role": usuario.role.value},
        ipOrigem=ipOrigem,
    )
    usuario_repo.registrarLog(db, log)

    return usuario


def atualizar(
    db: Session,
    usuarioId: uuid.UUID,
    dados: UsuarioUpdate,
    usuarioAtual: Usuario,
    ipOrigem: str | None = None,
) -> Usuario:
    usuario = usuario_repo.buscarPorId(db, str(usuarioId))
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "USUARIO_NAO_ENCONTRADO",
                "message": "Usuário não encontrado.",
                "details": [],
            },
        )

    if dados.nome is not None:
        usuario.nome = dados.nome
    if dados.ativo is not None:
        usuario.ativo = dados.ativo

    usuario_repo.atualizar(db, usuario)

    log = LogAuditoria(
        usuarioId=usuarioAtual.id,
        acao="ATUALIZAR_USUARIO",
        entidade="usuario",
        entidadeId=str(usuario.id),
        detalhe=dados.model_dump(exclude_none=True),
        ipOrigem=ipOrigem,
    )
    usuario_repo.registrarLog(db, log)

    return usuario


def listar(db: Session, skip: int = 0, limit: int = 10) -> list[Usuario]:
    return usuario_repo.listar(db, skip=skip, limit=limit)


def buscarPorId(db: Session, usuarioId: uuid.UUID) -> Usuario:
    usuario = usuario_repo.buscarPorId(db, str(usuarioId))
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "USUARIO_NAO_ENCONTRADO",
                "message": "Usuário não encontrado.",
                "details": [],
            },
        )
    return usuario