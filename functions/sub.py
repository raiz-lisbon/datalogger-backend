import json
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

from process_message import process_message

project_id = "environment-data"
subscription_id = "datalogger-sub"
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


# def callback(message):
#     device_id = message.attributes["device_id"]
#     device_type = message.attributes["device_type"]
#     data = json.loads(message.data.decode("utf-8"))

#     process_message(device_id, device_type, data)


streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_message)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
