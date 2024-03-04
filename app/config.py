from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    MS_SQL_HOST: str
    MS_SQL_PORT: int
    MS_SQL_USER: str
    MS_SQL_PASS: str
    MS_SQL_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def MS_SQL_CONNECTION_STRING(self):
        return f"mssql+aioodbc://{self.MS_SQL_USER}:{self.MS_SQL_PASS}@{self.MS_SQL_HOST}:{self.MS_SQL_PORT}/{self.MS_SQL_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"

    SECRET_KEY: str
    ALGORITM: str
    COOCKIES_NAME_TOKEN: str
    # Со 2 версии Pydantic, class Config был заменен на атрибут model_config
    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()