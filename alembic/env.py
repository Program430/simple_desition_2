import os

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.share.core.config import settings
from src.share.database.models.base import BaseSqlAlchemyModel
from src.share.database.models.ticker_price_model import TickerPriceModel # type[ignore]


config = context.config

section = config.config_ini_section

config.set_section_option(
    section, 'sqlalchemy.url', settings.database_url.replace('+asyncpg', '')
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = BaseSqlAlchemyModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
