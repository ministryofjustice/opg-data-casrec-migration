import configparser


def get_config(env="local"):
    config = configparser.ConfigParser()
    if env == "local":
        config.read("etl2/config/local_dev.cfg")

    return config
