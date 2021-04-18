""" This script handles python variables and defaults """
import os
import logging.config
import coloredlogs
from ruamel.yaml import YAML


# setup logger
def setup_logger():
    """ This function setups logger """
    yaml = YAML(typ='safe')

    # Create logs folder
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    if not os.path.isfile("./logging.yaml"):
        raise RuntimeError("You have to provide logging.yaml file in root directory")

    try:
        config = yaml.load("./logging.yaml")
        logging.config.dictConfig(config)
        coloredlogs.install()
    except Exception:  # pylint: disable=broad-except
        logging.basicConfig(level=logging.INFO)
        coloredlogs.install(level=logging.INFO)


# Load .env variables
SWAGGER_UI_URL = "http://134.122.71.130:8001/"
