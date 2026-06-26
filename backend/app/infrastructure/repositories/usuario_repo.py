from sqlalchemy.orm import Session
from app.domain.models.usuario import Usuario, ConsentimentoLgpd, LogAuditoria
from app.domain.enums import RoleEnum


def buscarPorEmail(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def buscarPorId(db: Session, usuarioId: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == usuarioId).first()


def listar(db: Session, skip: int = 0, limit: int = 10) -> list[Usuario]:
    return db.query(Usuario).offset(skip).limit(limit).all()


def criar(db: Session, usuario: Usuario) -> Usuario:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def atualizar(db: Session, usuario: Usuario) -> Usuario:
    db.commit()
    db.refresh(usuario)
    return usuario


def criarConsentimento(db: Session, consentimento: ConsentimentoLgpd) -> ConsentimentoLgpd:
    db.add(consentimento)
    db.commit()
    db.refresh(consentimento)
    return consentimento


def registrarLog(db: Session, log: LogAuditoria) -> LogAuditoria:
    db.add(log)
    db.commit()
    return log