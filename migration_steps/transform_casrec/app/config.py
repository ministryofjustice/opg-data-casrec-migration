import os


class BaseConfig:
    etl1_schema = "etl1"
    etl2_schema = "etl2"

    mapping_document = "docs/mapping_doc.xlsx"
    verbose = False
    row_limit = None


class LocalConfig(BaseConfig):
    connection_string = f"postgresql://casrec:casrec@localhost:6666/casrecmigration"  # pragma: allowlist secret
    VERBOSE = 5


class AWSConfig(BaseConfig):
    password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    name = os.environ.get("DB_NAME")

    connection_string = f"postgresql://casrec:{password}@{db_host}:{port}/{name}"  # pragma: allowlist secret


def get_config(env="local"):
    if env == "local":
        config = LocalConfig()
    else:
        config = AWSConfig()
    return config
