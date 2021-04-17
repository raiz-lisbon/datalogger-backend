import json
import random
from datetime import datetime
from google.cloud import pubsub_v1

project_id = "environment-data"
topic_id = "datalogger"
device_id = "RPI_0001"
device_type = "T_H"

publisher = pubsub_v1.PublisherClient(publisher_options=pubsub_v1.types.PublisherOptions(enable_message_ordering=True))
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

for n in range(1, 3):
    data = {
        "ts": datetime.now().timestamp(),
        "t": round(20 + 10 * random.random(), 2),
        "h": round(30 + 50 * random.random(), 2),
    }
    # Data must be a bytestring
    data = json.dumps(data).encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data, ordering_key="main", device_id=device_id, device_type=device_type)
    print(n, " sent")

print(f"Published messages to {topic_path}.")
