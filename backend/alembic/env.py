from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base
from app.models import User, Organization, Pet, InterestForm

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# --- NOVO CÓDIGO: Pegar DATABASE_URL do ambiente ---
def get_database_url():
    """Get database URL from environment or config file"""
    # Primeiro, tenta pegar da variável de ambiente
    database_url = os.environ.get("DATABASE_URL")
    
    if database_url:
        print(f"✅ Using DATABASE_URL from environment")
        return database_url
    
    # Se não tiver no ambiente, usa do arquivo de configuração
    database_url = config.get_main_option("sqlalchemy.url")
    if database_url:
        print(f"⚠️ Using DATABASE_URL from alembic.ini")
        return database_url
    
    raise ValueError("No DATABASE_URL found in environment or alembic.ini")

# --- NOVO CÓDIGO: Configurar a URL ---
database_url = get_database_url()
config.set_main_option("sqlalchemy.url", database_url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Adicionado para comparar tipos
        compare_server_default=True,  # Adicionado para comparar defaults
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Usa a URL configurada
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = database_url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Adicionado para detectar mudanças de tipo
            compare_server_default=True,  # Adicionado para detectar mudanças de default
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()