import os


class CasrecMigConfig:
    password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    name = os.environ.get("DB_NAME")
    user = os.environ.get("DB_USER")

    connection_string = f"postgresql://{user}:{password}@{db_host}:{port}/{name}"  # pragma: allowlist secret

    etl1_schema = "etl1"
    etl2_schema = "etl2"
    etl3_schema = "etl3"


class SiriusConfig:
    password = os.environ.get("SIRIUS_DB_PASSWORD")
    db_host = os.environ.get("SIRIUS_DB_HOST")
    port = os.environ.get("SIRIUS_DB_PORT")
    name = os.environ.get("SIRIUS_DB_NAME")
    user = os.environ.get("SIRIUS_DB_USER")

    connection_string = f"postgresql://{user}:{password}@{db_host}:{port}/{name}"  # pragma: allowlist secret
    sirius_schema = "public"


def get_config(env="local"):
    if env == "local":
        config = CasrecMigConfig()

    return config
