from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    appNome: str = Field("Gestao de Franquias API", alias="APP_NAME")
    appVersao: str = Field("1.0.0", alias="APP_VERSION")
    appEnv: str = Field("development", alias="APP_ENV")
    debug: bool = Field(True, alias="DEBUG")

    databaseUrl: str = Field(
        "postgresql://postgres:postgres@localhost:5432/gestao_franquias",
        alias="DATABASE_URL"
    )

    secretKey: str = Field("senhaProjeto123", alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="ALGORITHM")
    accessTokenExpireMinutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    pagamentoMockTaxaAprovacao: float = Field(0.8, alias="PAGAMENTO_MOCK_TAXA_APROVACAO")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "populate_by_name": True,
        "extra": "ignore",
    }


settings = Settings()