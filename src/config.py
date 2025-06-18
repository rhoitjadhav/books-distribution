import os

# Static Files
STATIC_FILES_PATH = "static"

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# Postgresql
SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)


class BaseConfig:
    # JWT Config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret-with-256-bits-long")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE = int(
        os.getenv(
            "JWT_ACCESS_TOKEN_EXPIRE", f"{60 * 24 * 7}"
        )  # Default to 7 day(s) in minutes
    )


def get_env_config(env: str = "dev"):
    mapping = {
        "dev": BaseConfig,
        "prod": BaseConfig,
        "test": BaseConfig,
    }
    return mapping.get(env, BaseConfig)
