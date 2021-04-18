import json
import random
from time import sleep
from datetime import datetime
from google.cloud import pubsub_v1


class Publisher:
    def __init__(self):
        self.project_id = "environment-data"
        self.topic_id = "datalogger"
        self.device_id = "RPI_0002"
        self.device_type = "T_H"
        self.batch_size = 1
        self.run_loop = True
        self.loop_count = 0
        self.data = []

        publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
        self.publisher = pubsub_v1.PublisherClient(publisher_options=publisher_options)
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

        self.get_data()

    def get_data(self):
        try:
            while self.run_loop:
                self.loop_count += 1
                if self.loop_count > 10000:
                    self.run_loop = False
                    return

                self.data.append(
                    {
                        "ts": datetime.now().timestamp(),
                        "t": round(20 + 10 * random.random(), 2),
                        "h": round(30 + 50 * random.random(), 2),
                    }
                )
                print(self.loop_count, "created, count", self.loop_count)
                self.publish()
                sleep(1)

        except Exception as e:
            print(e)

    def publish(self):
        try:
            if len(self.data) < self.batch_size:
                return

            data_to_publish = json.dumps(self.data).encode("utf-8")
            self.publisher.publish(
                self.topic_path,
                data_to_publish,
                ordering_key="main",
                device_id=self.device_id,
                device_type=self.device_type,
            )

            print(f"Published {len(self.data)} messages to {self.topic_path}.")

            self.data = []
        except Exception as e:
            print(e)


Publisher()
