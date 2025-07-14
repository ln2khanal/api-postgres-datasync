import json
import requests

# this is temorary data directoryto save the data pulled from Z server.
# This is used by the DataHandler class to save the data.
# This directory is mounted to the docker container.
# In the production server, the json files will be save to the S3 bucket.
from utils.constants import TEMPORARY_DATA_DIR

from .logger import get_console_logger

log = get_console_logger()


class DataHandler:
    def get_mapped_data(self, mapping: dict, data: dict) -> dict:
        """
        transforms the data from api structure to the database structure.
        excess fields in the data are accummulated in the notes field.
        Args:
            mapping: dict(<api_field>: <database_field>)
            data: dict(api_data)
        """
        _data = dict()

        try:
            for api_field, database_field in mapping.items():
                _data[database_field] = data.pop(api_field)
        except Exception as e:
            raise KeyError(f"Key mapping error: {e}")
        except KeyError as e:
            log.error(f"Key mapping error: {e}")

        # don't create a new field, that might break the API clients
        _data["notes"] = json.dumps(data)

        return _data

    def persist_json_response(self, json_data: dict, data_class: str) -> None:
        """saves the json data to a file in the temporary data directory.
        Args:
            json_data (dict): pulled data from the API.
            data_class (str): corresponding table name.
        """
        with open(f"{TEMPORARY_DATA_DIR}/{data_class}.json", "w") as f:
            f.write(json.dumps(json_data))

    def get_json_content(table_name: str) -> dict:
        """reads the json content from a json file in  the temporary data directory.
        Args:
            table_name (str): name of the table to read data from.
        """
        json_content = {}
        with open(f"{TEMPORARY_DATA_DIR}/{table_name}.json", "r") as f:
            try:
                json_content = json.loads(f.read())
            except json.JSONDecodeError as e:
                log.error(f"Error reading JSON content for {table_name}: {e}")
            except FileNotFoundError as e:
                log.error(f"File not found for {table_name}: {e}")
            except Exception as e:
                log.exception(f"Unexpected error reading {table_name}: {e}")
        return json_content


class APICaller:
    def __init__(self, url, payload={}):
        self.request_headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Host": "ExampleServer",
            "User-Agent": "Data Sync Agent",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Length": "0",
        }
        self.payload = payload
        self.url = url
        self.response = None
        self.status_code = None
        self.api_error = False

    def get(self):
        try:
            _res = requests.request(
                "GET", self.url, data=self.payload, headers=self.request_headers
            )
            self.status_code = _res.status_code
            self.response = _res.json()
        except Exception as e:
            self.status_code = 500
            self.response = {"message": e}

    def post(self):
        try:
            _res = requests.request(
                "POST", self.url, data=self.payload, headers=self.request_headers
            )
            self.status_code = _res.status_code
            self.response = _res.json()
        except Exception as e:
            self.status_code = 500
            self.response = {"message": e}
