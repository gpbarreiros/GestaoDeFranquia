from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.appNome,
    version=settings.appVersao,
)


@app.get("/", tags=["health"])
def root():
    return {
        "app": settings.appNome,
        "versao": settings.appVersao,
        "ambiente": settings.appEnv,
        "status": "ok",
    }


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
