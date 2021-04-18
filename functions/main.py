import json
from google.cloud import bigquery


def process_message_function(message, context):
    print(f"Function triggered by messageId {context.event_id} published at {context.timestamp}")

    try:
        client = bigquery.Client()

        project_id = "environment-data"
        dataset_id = "farm_one"

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
            schema_path = f"schemas/{device_type}.json"
            if schema_path.exists():
                schema = client.schema_from_json(schema_path)
            else:
                raise Exception(f"No schema found for {device_type}")

            table = bigquery.Table(table_ref, schema=schema)
            table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY, field="timestamp"
            )
            table = client.create_table(table)

        data_expanded = {"timestamp": data["ts"], "temperature": data["t"], "humidity": data["h"]}
        errors = client.insert_rows_json(table_path, [data_expanded])
        if errors == []:
            print("New row has been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))
    except Exception as e:
        print(e)
