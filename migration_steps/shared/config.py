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
        "remarks",
        "reporting",
        "tasks",
        "visits",
        "warnings",
        "death",
    ]

    LOCAL_FEATURE_FLAGS = {
        "match-existing-data": True,
        "additional-data": False,
        "row-counts": True,
        "generate-progress": False,
    }

    def enabled_feature_flags(self, env):
        if env in ["development", "preproduction", "qa", "preqa", "production"]:
            all_flags = list(self.LOCAL_FEATURE_FLAGS.keys())
            enabled_flags = list(
                flag
                for flag in all_flags
                if get_paramstore_value(f"{env}-{flag}") == "True"
            )
        else:
            enabled_flags = [
                k for k, v in self.LOCAL_FEATURE_FLAGS.items() if v is True
            ]
        return enabled_flags

    def allowed_entities(self, env):
        if env in ["development", "preproduction", "qa", "preqa", "production"]:
            entities = get_paramstore_value(f"{env}-allowed-entities")
            allowed_entity_list = entities.split(",")
        else:
            allowed_entity_list = self.LOCAL_ENTITIES

        if len(allowed_entity_list) > 0:
            return allowed_entity_list
        else:
            log.error("No entities allowed")
            os._exit(1)

    def get_filtered_lay_team(self, env, console_team):
        filter_team = ""

        if env in ["development", "preproduction", "preqa", "qa", "production"]:
            param_team = get_paramstore_value(f"{env}-lay-team")
            if param_team in ["0", "all", "All", "ALL"]:
                log.info(f"No filtering requested, proceed with migrating ALL.")
            else:
                filter_team = param_team
                log.info(
                    f"Lay Team filtering specified in param store: Team {param_team}"
                )

        if console_team:
            log.info(f"Lay Team filtering requested at runtime: Team {console_team}")
            filter_team = console_team

        return filter_team


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
