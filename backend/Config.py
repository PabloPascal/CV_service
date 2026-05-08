


class Config:
    DATABASE_URL: str = "postgresql+asyncpg://user:fake_password@localhost:5432/dbname"
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

    



settings = Config()

