import os
import sys
from pathlib import Path
import logging.config
import time
from dotenv import load_dotenv
import click
from counts_verification import CountsVerification

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import custom_logger
import helpers

env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)
environment = os.environ.get("ENVIRONMENT")
config = helpers.get_config(env=environment)

custom_logger.setup_logging(
    env=environment,
    module_name="Count client-pilot-one data",
)
log = logging.getLogger("root")
config.custom_log_level()


def output_title(correfs):
    allowed_entities = config.allowed_entities(env=environment)
    filtered_correfs = config.get_filtered_correfs(environment, correfs)
    log.info(helpers.log_title(message="Counts Verification: Pre-Migration counts"))
    log.debug(f"Environment: {environment}")
    log.info(f"Correfs: {', '.join(filtered_correfs) if filtered_correfs else 'all'}")
    log.info(f"Enabled entities: {', '.join(allowed_entities)}")
    log.info(
        f"Enabled features: {', '.join(config.enabled_feature_flags(environment))}"
    )
    log.info(helpers.log_title(message="Begin"))


@click.command()
@click.option("--correfs", default="")
@click.option("--stage")
def main(correfs, stage):
    output_title(correfs)

    counter = CountsVerification()
    counter.call_stage(stage)


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
