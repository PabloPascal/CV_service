

class Settings:
    DATABASE_URL: str = "postgresql+asyncpg://Pablo:1248@database:5432/my_DB"
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

    



settings = Settings()

