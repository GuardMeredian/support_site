from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    EOBD_HOST: str
    EOBD_PORT: int
    EOBD_USER: str
    EOBD_PASS: str
    EOBD_NAME: str
    AKTPAK_NAME: str

    EOBD_TEMP_NAME: str
    EOBD_TEST_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def MS_SQL_CONNECTION_STRING(self):
        return f"mssql+aioodbc://{self.EOBD_USER}:{self.EOBD_PASS}@{self. EOBD_HOST}:{self.EOBD_PORT}/{self.EOBD_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    
    @property
    def AKTPAK_MS_SQL_CONNECTION_STRING(self):
        return f"mssql+aioodbc://{self.EOBD_USER}:{self.EOBD_PASS}@{self. EOBD_HOST}:{self.EOBD_PORT}/{self. AKTPAK_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    
    @property
    def TEMP_MS_SQL_CONNECTION_STRING(self):
        return f"mssql+aioodbc://{self.EOBD_USER}:{self.EOBD_PASS}@{self. EOBD_HOST}:{self.EOBD_PORT}/{self.EOBD_TEMP_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    
    @property
    def TEST_MS_SQL_CONNECTION_STRING(self):
        return f"mssql+aioodbc://{self.EOBD_USER}:{self.EOBD_PASS}@{self. EOBD_HOST}:{self.EOBD_PORT}/{self.EOBD_TEST_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"

    SECRET_KEY: str
    ALGORITM: str
    COOCKIES_NAME_TOKEN: str
    # Со 2 версии Pydantic, class Config был заменен на атрибут model_config
    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()