from fastapi import APIRouter, Request
from app.api.deps import DbDep
from app.schemas.auth import LoginRequest, TokenResponse
from app.application import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest, request: Request, db: DbDep):
    return auth_service.login(db, dados.email, dados.senha)