import uuid
from typing import Optional
from sqlalchemy import String, Boolean, Enum as SAEnum, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.infrastructure.database import Base
from app.domain.enums import RoleEnum, BaseLegalEnum


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )
    senhaHash: Mapped[str] = mapped_column(
        "senha_hash",
        String(255),
        nullable=False,
    )
    role: Mapped[RoleEnum] = mapped_column(
        SAEnum(RoleEnum, name="role_enum"),
        nullable=False,
    )
    baseLegalTratamento: Mapped[BaseLegalEnum] = mapped_column(
        "base_legal_tratamento",
        SAEnum(BaseLegalEnum, name="base_legal_enum"),
        nullable=False,
    )
    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    criadoEm: Mapped[DateTime] = mapped_column(
        "criado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relacionamentos
    consentimentosLgpd: Mapped[list["ConsentimentoLgpd"]] = relationship(
        "ConsentimentoLgpd",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
    pedidos: Mapped[list["Pedido"]] = relationship(
        "Pedido",
        back_populates="cliente",
        foreign_keys="Pedido.clienteId",
    )
    fidelidade: Mapped[Optional["Fidelidade"]] = relationship(
        "Fidelidade",
        back_populates="cliente",
        uselist=False,
    )
    logsAuditoria: Mapped[list["LogAuditoria"]] = relationship(
        "LogAuditoria",
        back_populates="usuario",
    )
    movimentacoesEstoque: Mapped[list["MovimentacaoEstoque"]] = relationship(
        "MovimentacaoEstoque",
        back_populates="usuario",
    )

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email} role={self.role}>"


class ConsentimentoLgpd(Base):
    __tablename__ = "consentimento_lgpd"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    usuarioId: Mapped[uuid.UUID] = mapped_column(
        "usuario_id",
        UUID(as_uuid=True),
        ForeignKey("usuario.id", ondelete="CASCADE"),
        nullable=False,
    )
    finalidade: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    aceito: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    registradoEm: Mapped[DateTime] = mapped_column(
        "registrado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relacionamento
    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="consentimentosLgpd",
    )

    def __repr__(self) -> str:
        return (
            f"<ConsentimentoLgpd usuarioId={self.usuarioId} "
            f"aceito={self.aceito}>"
        )


class LogAuditoria(Base):
    __tablename__ = "log_auditoria"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    usuarioId: Mapped[Optional[uuid.UUID]] = mapped_column(
        "usuario_id",
        UUID(as_uuid=True),
        ForeignKey("usuario.id", ondelete="SET NULL"),
        nullable=True,        # ação pode vir de sistema sem usuário logado
    )
    acao: Mapped[str] = mapped_column(String(100), nullable=False)
    entidade: Mapped[str] = mapped_column(String(100), nullable=False)
    entidadeId: Mapped[Optional[str]] = mapped_column(
        "entidade_id",
        String(36),
        nullable=True,
    )
    detalhe: Mapped[Optional[dict]] = mapped_column(
        "detalhe",
        JSONB,
        nullable=True,
    )
    ipOrigem: Mapped[Optional[str]] = mapped_column(
        "ip_origem",
        String(45),           # suporta IPv6
        nullable=True,
    )
    criadoEm: Mapped[DateTime] = mapped_column(
        "criado_em",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relacionamento
    usuario: Mapped[Optional["Usuario"]] = relationship(
        "Usuario",
        back_populates="logsAuditoria",
    )

    def __repr__(self) -> str:
        return (
            f"<LogAuditoria acao={self.acao} "
            f"entidade={self.entidade} id={self.entidadeId}>"
        )