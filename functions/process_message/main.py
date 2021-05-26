import json
import base64
from google.cloud import bigquery
from google.cloud import error_reporting
from google.cloud.exceptions import NotFound

error_client = error_reporting.Client()
bigquery_client = bigquery.Client()

project_id = "environment-data"


def get_or_create_dataset(message):
    dataset_id = message["attributes"]["dataset_id"]
    dataset_ref = f"{project_id}.{dataset_id}"

    try:
        dataset = bigquery_client.get_dataset(dataset_ref)
        return dataset
    except NotFound:
        print(f"Dataset {dataset_id} not found, creating...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "EU"
        dataset = bigquery_client.create_dataset(dataset)
        print(f"Created dataset {dataset_ref}")
        return dataset


def get_or_create_table(message, dataset):
    device_id = message["attributes"]["device_id"]
    device_type = message["attributes"]["device_type"]
    table_id = f"{device_id}_{device_type}"

    table_ref = f"{project_id}.{dataset.dataset_id}.{table_id}"

    try:
        table = bigquery_client.get_table(table_ref)
        return False, table
    except NotFound:
        print(f"Table {table_id} not found, creating...")
        table = bigquery.Table(table_ref)
        table = bigquery_client.create_table(table)
        print(f"Created table {table_ref}")
        return True, table


def init_table(table, data):
    job_config = bigquery.LoadJobConfig(autodetect=True, source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)
    load_job = bigquery_client.load_table_from_json(json_rows=data, destination=table, job_config=job_config)
    load_job.result()


def process_message(message, context):
    print(f"Function triggered by messageId {context.event_id} published at {context.timestamp}")
    try:
        data = json.loads(base64.b64decode(message["data"]).decode("utf-8"))

        dataset = get_or_create_dataset(message)
        should_init_table, table = get_or_create_table(message, dataset)

        if should_init_table:
            init_table(table, data)
        else:
            bigquery_client.insert_rows_json(table, json_rows=data)
            print(f"{len(data)} rows added to {table.table_id}")

    except Exception as e:
        error_client.report_exception()
        print(e)
