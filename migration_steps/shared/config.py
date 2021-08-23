import logging
import os
import boto3
from pathlib import Path
from deprecated import deprecated
from dotenv import load_dotenv

log = logging.getLogger("root")


def load_env_vars():
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    env_path = current_path / "../.env"
    load_dotenv(dotenv_path=env_path)


def get_enabled_entities_from_param_store(env):
    session = boto3.session.Session()
    ssm = session.client("ssm", region_name="eu-west-1")
    parameter = ssm.get_parameter(Name=f"{env}-allowed-entities")

    return parameter["Parameter"]["Value"].split(",")


class BaseConfig:
    load_env_vars()
    db_config = {
        "migration": {
            "host": os.environ.get("DB_HOST"),
            "port": os.environ.get("DB_PORT"),
            "name": os.environ.get("DB_NAME"),
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
        },
        "target": {
            "host": os.environ.get("SIRIUS_DB_HOST"),
            "port": os.environ.get("SIRIUS_DB_PORT"),
            "name": os.environ.get("SIRIUS_DB_NAME"),
            "user": os.environ.get("SIRIUS_DB_USER"),
            "password": os.environ.get("SIRIUS_DB_PASSWORD"),
        },
    }

    schemas = {
        "pre_transform": "casrec_csv",
        "post_transform": "transform",
        "integration": "integration",
        "public": "public",
        "pre_migration": "staging",
    }

    row_limit = 5

    VERBOSE = 5
    DATA = 2
    verbosity_levels = {0: "INFO", 1: "DEBUG", 2: "VERBOSE"}

    def verbose(self, msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(self.VERBOSE):
            logging.log(self.VERBOSE, msg)

    @deprecated(
        version="1", reason="You should use custom_logger.setup_logging instead"
    )
    def custom_log_level(self):
        logging.addLevelName(self.VERBOSE, "VERBOSE")
        logging.Logger.verbose = self.verbose

    def get_db_connection_string(self, db):
        return (
            f"postgresql://{self.db_config[db]['user']}:{self.db_config[db]['password']}@"
            f"{self.db_config[db]['host']}:{self.db_config[db]['port']}"
            f"/{self.db_config[db]['name']}"
        )  # pragma: allowlist secret

    DEFAULT_CHUNK_SIZE = int(os.environ.get("DEFAULT_CHUNK_SIZE", 20000))

    ALL_ENVIRONMENTS = ["local", "development", "preproduction", "qa", "preqa"]
    ENABLED_ENTITIES = {
        "clients": ["local", "development"],
        "cases": ["local", "development"],
        "bonds": ["local", "development"],
        "crec": ["local", "development"],
        "supervision_level": ["local", "development"],
        "deputies": ["local", "development"],
        "invoice": ["local"],
        "remarks": ["local", "development"],
        "reporting": ["local", "development"],
        "tasks": [],
        "visits": ["local", "development"],
        "warnings": ["local", "development"],
        "death": ["local", "development"],
    }

    DEV_FEATURE_FLAGS = {
        "match_existing_data": True,
        "additional_data": False,
        "row_counts": True,
        "generate_progress": False,
    }
    QA_FEATURE_FLAGS = {}

    def enabled_feature_flags(self, env):

        if env in ["qa", "production"]:
            return [k for k, v in self.QA_FEATURE_FLAGS.items() if v is True]
        else:
            return [k for k, v in self.DEV_FEATURE_FLAGS.items() if v is True]

    def allowed_entities(self, env):
        if env in ["preproduction", "qa", "preqa", "production"]:
            enabled_entity_list = get_enabled_entities_from_param_store(env)
        else:
            enabled_entity_list = [
                k for k, v in self.ENABLED_ENTITIES.items() if env in v
            ]

        if len(enabled_entity_list) > 0:
            return enabled_entity_list
        else:
            log.error("No entities enabled")
            os._exit(1)


class LocalConfig(BaseConfig):
    verbosity_levels = {0: "INFO", 1: "DEBUG", 2: "VERBOSE", 3: "DATA"}
    SAMPLE_PERCENTAGE = 10
    MIN_PERCENTAGE_FIELDS_TESTED = 96  # 100 would be better but not there yet!

    def data(self, msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(self.DATA):
            logging.log(self.DATA, msg)

    @deprecated(
        version="1", reason="You should use custom_logger.setup_logging instead"
    )
    def custom_log_level(self):
        logging.addLevelName(self.VERBOSE, "VERBOSE")
        logging.Logger.verbose = self.verbose

        logging.addLevelName(self.DATA, "DATA")
        logging.Logger.data = self.data


def get_config(env="local"):
    if env == "local":
        config = LocalConfig()
    else:
        config = BaseConfig()
    return config
