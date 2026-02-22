from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    api_version: str
    debug: bool
    log_level: str

    redis_host: str
    redis_port: int
    redis_db: int

    redis_celery_broker_db: str

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    client_base_url: str

    @property
    def redis_base(self) -> str:
        return f'redis://{self.redis_host}:{self.redis_port}'

    @property
    def redis_url(self) -> str:
        return f'{self.redis_base}/{self.redis_db}'

    @property
    def redis_celery_broker_url(self) -> str:
        return f'{self.redis_base}/{self.redis_celery_broker_db}'

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )


settings = Settings()  # type: ignore[call-arg]
