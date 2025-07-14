import sys
import time

from pathlib import Path
from utils.logger import get_console_logger
from pull_server.pull_data import DataPuller
from utils.constants import TEMPORARY_DATA_DIR
from push_server import push_to_database as data_pusher
from authentication.auth import retrieve_bearer_token

log = get_console_logger()


def lambda_handler(event: dict = None, context=None):
    if any(Path(TEMPORARY_DATA_DIR).glob("*.json")):
        log.info("Temporary data directory is not empty. Exiting, check for errors.")
        sys.exit(1)

    bearer_token = retrieve_bearer_token()
    log.info(f"Bearer Token: {bearer_token[:4]}...{bearer_token[-4:]}")

    if not bearer_token:
        log.error("Bearer token is required for API requests")
        sys.exit(1)

    data_puller = DataPuller()

    log.info(f"Setting authentication token: {bearer_token[:4]}...{bearer_token[-4:]}")
    data_puller.set_bearer_token(token=bearer_token)

    log.info("Pulling patient, prescription and stock level from Z server.")
    data_puller.pull()

    log.info("Syncing pull data to database server.")
    data_pusher.push()
    log.info("A data sync cycle completed.")


def init():
    """
    This function is not applicable in the production server.
    In the production setup, AWS lambda will activate lambda_handler.
    In the lambda, two lambdas will be used.
    One pulls that data from Z and another will push pulled data to database.
    ECS if used will use the same entry point. Remove the wait logic.
    """
    log.info("Starting the database sync service...")
    wait_interval = 10 * 60
    while True:
        log.info("executing lambda_handler")
        lambda_handler()
        log.info(f"Waiting for next {wait_interval} seconds")
        time.sleep(wait_interval)


if __name__ == "__main__":
    init()
