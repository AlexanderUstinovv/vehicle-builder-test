from pydantic import BaseSettings


class DBSettings(BaseSettings):
    """Database env variables"""

    USER: str
    PASSWORD: str
    NAME: str
    HOST: str
    PORT: int
    DIALECT: str = "postgresql"

    class Config:
        env_prefix = "DB_"
        env_file = ".env"
        env_file_encoding = "utf-8"


config = DBSettings()


DATABASE_URL = (
    f"{config.DIALECT}://{config.USER}:{config.PASSWORD}@{config.HOST}:{config.PORT}/{config.NAME}"
)
