import json
from pathlib import Path
from google.cloud import bigquery

client = bigquery.Client()

project_id = "environment-data"
dataset_id = "farm_one"


def process_message(message):
    device_id = message.attributes["device_id"]
    device_type = message.attributes["device_type"]
    data = json.loads(message.data.decode("utf-8"))

    # Construct table name and path
    table_name = f"{device_id}_{device_type}"
    table_path = f"{project_id}.{dataset_id}.{table_name}"

    # Create table if does not exist
    tables = client.list_tables(dataset_id)
    table_names = [table.table_id for table in tables]
    if table_name not in table_names:
        dataset_ref = bigquery.DatasetReference(client.project, dataset_id)
        table_ref = dataset_ref.table(table_name)

        # Retrieve database schema for provided device_type
        schema_path = Path(__file__).parent.joinpath(f"schemas/{device_type}.json").absolute()
        if schema_path.exists():
            schema = client.schema_from_json(schema_path)
        else:
            raise Exception(f"No schema found for {device_type}")

        table = bigquery.Table(table_ref, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.DAY, field="timestamp")
        table = client.create_table(table)

    data_expanded = {"timestamp": data["ts"], "temperature": data["t"], "humidity": data["h"]}
    errors = client.insert_rows_json(table_path, [data_expanded])
    if errors == []:
        print("New rows have been added.")
        message.ack()
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
