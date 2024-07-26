from kafka import KafkaConsumer
from json import dumps
from kafka_parser import Parser


import sys

sys.path.append("/home/lfgomes/group-project-s22-dsu")
import db_manager as db

enable_commit = False
auto_commit_interval = 1000
max_num_messages = 1000


# Create a consumer to read data from kafka

if enable_commit:
    consumer = KafkaConsumer(
        "movielog4",
        bootstrap_servers=["localhost:9092"],
        # Read from the start of the topic; Default is latest
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        # How often to tell Kafka, an offset has been read
        auto_commit_interval_ms=auto_commit_interval,
    )
else:
    consumer = KafkaConsumer(
        "movielog4",
        bootstrap_servers=["localhost:9092"]
        # Read from the start of the topic; Default is latest
        # auto_offset_reset='earliest',
    )


print("In consumer.py")
parser = Parser()
# Prints all messages, again and again!
for i, message in enumerate(consumer):
    # Default message.value type is bytes!
    out_json = dumps(parser.parse(message.value.decode("utf-8")))
    db.insert_new_entry(out_json)
    # print(out_json)
    # if i > max_num_messages:
    #     break
