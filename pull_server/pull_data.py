from utils.common_class import APICaller
from utils.common_class import DataHandler
from utils.constants import SUCCESS_STATUS_CODE, SUPPORTED_TABLE_MAPPINGS
from utils.constants import PATIENT_URL, PRESCRIPTION_URL, STOCK_URL

from utils.logger import get_console_logger

log = get_console_logger()


class DataPuller(DataHandler):
    def __init__(self):
        super().__init__()
        self.api_caller = APICaller(url="", payload={})

    def set_bearer_token(self, token):
        self.api_caller.request_headers.update({"Authorization": f"Bearer {token}"})

    def pull_patient(self, payload={}):
        self.api_caller.url = PATIENT_URL
        self.api_caller.payload = payload
        self.api_caller.get()
        self.persist_json_response(
            json_data=self.api_caller.response, data_class="patient"
        )

    def pull_prescription(self, payload={}):
        self.api_caller.url = PRESCRIPTION_URL
        self.api_caller.payload = payload
        self.api_caller.get()
        self.persist_json_response(
            json_data=self.api_caller.response, data_class="prescription"
        )

    def pull_stock(self, payload={}):
        self.api_caller.url = STOCK_URL
        self.api_caller.payload = payload
        self.api_caller.get()
        self.persist_json_response(
            json_data=self.api_caller.response, data_class="stock"
        )

    def pull(self):
        """
        Pulls data for each supported table by invoking the corresponding pull method.

        Iterates over all table names defined in SUPPORTED_TABLE_MAPPINGS, logs the start of each pull operation,
        and calls the respective pull method (e.g., pull_<table_name>). After each pull, checks the API caller's
        status code; if the pull was unsuccessful, logs an error message indicating the failure.

        Raises:
            Logs an error if data for any table could not be pulled successfully.
        """
        for table_name in SUPPORTED_TABLE_MAPPINGS.keys():
            log.info(f"pulling table data={table_name}")
            getattr(self, f"pull_{table_name}")()
            if self.api_caller.status_code is not SUCCESS_STATUS_CODE:
                log.error(
                    f"Error: {table_name} data were not pulled, check for errors in console"
                )
