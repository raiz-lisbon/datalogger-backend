import json
import random
from time import sleep
from datetime import datetime
from google.cloud import pubsub_v1


class Publisher:
    def __init__(self):
        self.project_id = "environment-data"
        self.topic_id = "datalogger"
        self.device_id = "RPI_0001"
        self.device_type = "T_H"
        self.batch_size = 5
        self.run_loop = True
        self.loop_count = 0
        self.data = []

        batch_settings = pubsub_v1.types.BatchSettings(max_messages=60, max_latency=60000)
        self.publisher = pubsub_v1.PublisherClient(batch_settings)
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

        self.get_data()

    def get_data(self):
        print("asd", self.run_loop)
        while self.run_loop:
            self.data.append(
                {
                    "ts": datetime.now().timestamp(),
                    "t": round(20 + 10 * random.random(), 2),
                    "h": round(30 + 50 * random.random(), 2),
                }
            )
            print(self.loop_count, "created")
            self.publish()
            self.loop_count += 1
            sleep(1)

            if self.loop_count > 100:
                self.run_loop = False

    def publish(self):
        if len(self.data) < self.batch_size:
            return

        data_to_publish = json.dumps(self.data).encode("utf-8")
        self.publisher.publish(self.topic_path, data_to_publish, device_id=self.device_id, device_type=self.device_type)

        print(f"Published {len(self.data)} messages to {self.topic_path}.")

        self.data = []


Publisher()
