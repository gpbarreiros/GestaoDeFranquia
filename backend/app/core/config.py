from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional


class Settings(BaseSettings):
    # Aplicação
    appNome: str = "Gestão de Franquias API"
    appVersao: str = "1.0.0"
    appEnv: str = "development"
    debug: bool = True

    # Banco de dados
    postgresHost: str = "localhost"
    postgresPort: int = 5432
    postgresDb: str = "gestao_franquias"
    postgresUser: str = "postgres"
    postgresPassword: str = "postgres"
    databaseUrl: Optional[str] = None

    @field_validator("databaseUrl", mode="before")
    @classmethod
    def montar_database_url(cls, v, info):
        if v:
            return v
        dados = info.data
        return (
            f"postgresql://{dados.get('postgresUser')}"
            f":{dados.get('postgresPassword')}"
            f"@{dados.get('postgresHost')}"
            f":{dados.get('postgresPort')}"
            f"/{dados.get('postgresDb')}"
        )

    # JWT
    secretKey: str = "troque-esta-chave-em-producao"
    algorithm: str = "HS256"
    accessTokenExpireMinutes: int = 60

    # Gateway mock
    pagamentoMockTaxaAprovacao: float = 0.8

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "populate_by_name": True,
        "extra": "ignore",
    }


settings = Settings()