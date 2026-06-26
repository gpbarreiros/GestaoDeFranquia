from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import LogMiddleware
from app.api.v1 import router

app = FastAPI(
    title=settings.appNome,
    version=settings.appVersao,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(LogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "versao": settings.appVersao}