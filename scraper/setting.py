import logging
import os

BASE_URL = os.getenv('BASE_URL')

# influxdb config
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_URL = os.getenv('INFLUXDB_URL')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')


# logging config
def get_logger(name, log_level=logging.INFO):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to console handler
    ch.setFormatter(formatter)

    # add console handler to logger
    logger.addHandler(ch)

    return logger
