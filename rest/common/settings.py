""" This script handles python variables and defaults """
import os
import logging.config


# setup logger
def setup_logger():
    """ This function setups logger """

    # Create logs folder
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    logging.basicConfig(filename='./logs/app.log',
                        filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')


# Load .env variables
SWAGGER_UI_URL = "http://134.122.71.130:8001/"
