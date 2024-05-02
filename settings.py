from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: int
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DB: str
    DATABASE_USER_COLLECTION: str
    DATABASE_AUTH_COLLECTION: str
    AUTH_SECRET_KEY: str


settings = Settings()
