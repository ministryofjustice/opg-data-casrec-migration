class BaseConfig:
    mapping_document = "etl2/docs/mapping_doc.xlsx"
    verbose = False
    row_limit = None


class LocalConfig(BaseConfig):
    connection_string = "postgresql://casrec:casrec@0.0.0.0:6666/casrecmigration"  # pragma: allowlist secret
    etl1_schema = "etl1"
    etl2_schema = "etl2"


def get_config(env="local"):
    if env == "local":
        config = LocalConfig()

    return config
