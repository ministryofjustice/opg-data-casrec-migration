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


def get_paramstore_value(param_name):
    session = boto3.session.Session()
    ssm = session.client("ssm", region_name="eu-west-1")
    parameter = ssm.get_parameter(Name=param_name)
    return parameter["Parameter"]["Value"]


class BaseConfig:
    load_env_vars()
    db_config = {
        "casrec": {
            "host": os.environ.get("CASREC_DB_HOST"),
            "port": os.environ.get("CASREC_DB_PORT"),
            "name": os.environ.get("CASREC_DB_NAME"),
            "user": os.environ.get("CASREC_DB_USER"),
            "password": os.environ.get("CASREC_DB_PASSWORD"),
        },
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
        "count_verification": "countverification",
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

    ALL_ENVIRONMENTS = [
        "local",
        "development",
        "preproduction",
        "qa",
        "preqa",
        "rehearsal",
        "production",
    ]
    LOCAL_ENTITIES = [
        "clients",
        "cases",
        "bonds",
        "crec",
        "supervision_level",
        "deputies",
        "invoice",
        "ledger",
        "ledger_allocation",
        "fee_reductions",
        "finance_order",
        "remarks",
        "reporting",
        "tasks",
        "timeline",
        "visits",
        "warnings",
        "death",
        "scheduled_events",
    ]

    LOCAL_FEATURE_FLAGS = {
        "match-existing-data": True,
        "additional-data": False,
        "generate-progress": False,
    }

    def enabled_feature_flags(self, env):
        if env is None or env == "local":
            enabled_flags = [
                k for k, v in self.LOCAL_FEATURE_FLAGS.items() if v is True
            ]
        else:
            all_flags = list(self.LOCAL_FEATURE_FLAGS.keys())
            enabled_flags = list(
                flag
                for flag in all_flags
                if get_paramstore_value(f"{env}-{flag}") == "True"
            )
        return enabled_flags

    def allowed_entities(self, env):
        if env is None or env == "local":
            allowed_entity_list = self.LOCAL_ENTITIES
        else:
            entities = get_paramstore_value(f"{env}-allowed-entities")
            allowed_entity_list = entities.split(",")

        if len(allowed_entity_list) > 0:
            return allowed_entity_list
        else:
            log.error("No entities allowed")
            os._exit(1)

    def get_filtered_correfs(self, env, console_correfs):
        filter_correfs = ""

        if env is None or env == "local":
            pass
        else:
            param_correfs = get_paramstore_value(f"{env}-correfs")
            if param_correfs == "0":
                log.info(f"No filtering requested, proceed with migrating all Correfs.")
            else:
                filter_correfs = param_correfs
                log.info(f"Corref filtering specified in param store: {filter_correfs}")

        if console_correfs:
            filter_correfs = console_correfs
            log.info(f"Corref filtering requested at runtime: {console_correfs}")

        if not filter_correfs:
            return []

        return [corref.strip() for corref in filter_correfs.split(",")]


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
