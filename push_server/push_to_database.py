from pathlib import Path

from psycopg2.extras import execute_batch

from utils.common_class import DataHandler
from authentication.auth import get_db_connection
from utils.logger import get_console_logger as log
from utils.constants import SUPPORTED_TABLE_MAPPINGS, TEMPORARY_DATA_DIR


def push():
    conn = get_db_connection()
    cursor = conn.cursor()
    data_handler = DataHandler()
    try:
        for table_name in SUPPORTED_TABLE_MAPPINGS.keys():
            data = data_handler.get_json_content(table_name=table_name)
            mapped_data = data_handler.get_mapped_data(
                mapping=SUPPORTED_TABLE_MAPPINGS[table_name], data=data
            )
            _sync(conn=conn, cursor=cursor, table_name=table_name, data=mapped_data)
            log.info(f"Data synced, flushing table data: {table_name}")
            _flush_data(data_class=table_name)
    except Exception as e:
        log.critical(f"Error; data couldn't be inserted, table={table_name}, error={e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def _sync(conn, cursor, table_name, data):
    log.debug(f"Will save: Table={table_name} Data={data}")

    columns = data.keys()
    values = list(data.values())
    placeholders = ", ".join(["%s"] * len(values))
    insert_query = (
        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    )

    execute_batch(cursor, insert_query, data)
    conn.commit()


def _flush_data(data_class: str):
    """Flushes the data from the temporary directory."""
    file_path = f"{TEMPORARY_DATA_DIR}/{data_class}.json"
    try:
        if Path(file_path).exists():
            Path(file_path).unlink()
            log.info(f"Flushed data file: {file_path}")
    except Exception as e:
        log.error(f"Error flushing data file: {file_path}, {e}")
