import os
import warnings
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy.exc import SAWarning

from database import Base
from repositories import *  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

warnings.filterwarnings(
    "ignore", category=SAWarning, message="Did not recognize type 'geometry'"
)

url = os.getenv("SQLALCHEMY_DATABASE_URL") or context.config.get_main_option(
    "sqlalchemy.url"
)
context.config.set_main_option("sqlalchemy.url", url)


def include_object(object, name, type_, reflected, compare_to):
    exclude_tables = {
        "spatial_ref_sys",
        "zip_lookup_all",
        "bg",
        "state_lookup",
        "faces",
        "zip_lookup",
        "county_lookup",
        "edges",
        "geocode_settings",
        "addrfeat",
        "featnames",
        "pagc_gaz",
        "layer",
        "state",
        "zip_lookup_base",
        "street_type_lookup",
        "loader_platform",
        "zip_state_loc",
        "pagc_rules",
        "zcta5",
        "countysub_lookup",
        "topology",
        "tabblock20",
        "secondary_unit_lookup",
        "loader_lookuptables",
        "place",
        "county",
        "geocode_settings_default",
        "tabblock",
        "tract",
        "addr",
        "cousub",
        "zip_state",
        "pagc_lex",
        "loader_variables",
        "place_lookup",
        "direction_lookup",
    }

    if type_ == "table" and name in exclude_tables:
        return False

    # Skip indexes related to excluded tables
    if (
        type_ == "index"
        and hasattr(object, "table")
        and object.table.name in exclude_tables
    ):
        return False

    # Skip sequences endswith "_gid_seq" for specific tables
    if type_ == "sequence" and name.endswith("_gid_seq"):
        return False

    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
