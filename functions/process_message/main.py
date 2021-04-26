import json
import base64
from pathlib import Path
from google.cloud import bigquery
from google.cloud import error_reporting

error_client = error_reporting.Client()
client = bigquery.Client()

project_id = "environment-data"
dataset_id = "farm_one"


def process_message(message, context):
    print(f"Function triggered by messageId {context.event_id} published at {context.timestamp}")
    try:
        device_id = message["attributes"]["device_id"]
        device_type = message["attributes"]["device_type"]
        data = json.loads(base64.b64decode(message["data"]).decode("utf-8"))

        # Construct table name and path
        table_name = f"{device_id}_{device_type}"
        dataset_ref = bigquery.DatasetReference(client.project, dataset_id)
        table_ref = dataset_ref.table(table_name)

        # Create table if does not exist
        tables = client.list_tables(dataset_id)
        table_names = [table.table_id for table in tables]
        if table_name not in table_names:
            table = bigquery.Table(table_ref)
            client.create_table(table)

        job_config = bigquery.LoadJobConfig(autodetect=True, source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)
        load_job = client.load_table_from_json(json_rows=data, destination=table_ref, job_config=job_config)
        load_job.result()

        print(f"{len(data)} rows added to {project_id}.{dataset_id}.{table_name}")
    except Exception as e:
        client.report_exception()
        print(e)
