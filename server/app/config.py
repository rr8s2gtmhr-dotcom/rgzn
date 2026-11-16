from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # 本地开发使用 DB_* 变量；Railway MySQL 注入 MYSQLHOST/MYSQLPORT/...
    # AliasChoices 让两者都可用，无需在平台手动改变量名。
    DB_HOST: str = Field(default="127.0.0.1", validation_alias=AliasChoices("DB_HOST", "MYSQLHOST"))
    DB_PORT: int = Field(default=3306, validation_alias=AliasChoices("DB_PORT", "MYSQLPORT"))
    DB_USER: str = Field(default="root", validation_alias=AliasChoices("DB_USER", "MYSQLUSER"))
    DB_PASSWORD: str = Field(default="", validation_alias=AliasChoices("DB_PASSWORD", "MYSQLPASSWORD"))
    DB_NAME: str = Field(default="rgzn-ai", validation_alias=AliasChoices("DB_NAME", "MYSQLDATABASE"))
    DB_CHARSET: str = "utf8mb4"

    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_SECONDS: int = 86400

    CORS_ORIGINS: str = "*"

    @property
    def database_url(self) -> str:
        from sqlalchemy.engine import URL

        return URL.create(
            "mysql+aiomysql",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
            query={"charset": self.DB_CHARSET},
        )


settings = Settings()
