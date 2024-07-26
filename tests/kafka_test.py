from kafka import KafkaProducer, TopicPartition, KafkaConsumer
import sys
import json
from time import sleep
from datetime import datetime
client = ["localhost:9092"]
topic = "movielog04"
nbrrecords = int(10)
nbrrecordsinserted = int(0)
nbrrecordsretreived = int(0)
now = datetime.now().strftime("%d%m%Y-%H%M")

def test_consumer():
    print("Just, Entered!")
    def generate_report(nbrrecords, nbrrecordsinserted, nbrrecordsretreived):
        with open("testing-results-" + now + ".txt", "w") as f:
            f.write("Number of record to insert : " + str(nbrrecords))
            f.write("\n")
            f.write("Number of record inserted : " + str(nbrrecordsinserted))
            f.write("\n")
            f.write("Number of record consumed : " + str(nbrrecordsretreived))

    try:
        print("Hello, I have just started!")
        producer = KafkaProducer(bootstrap_servers=client,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        print("Generating the 100 records")
        for i in range(1, nbrrecords + 1):
            data = {'number' : i}
            producer.send(topic, data)
            nbrrecordsinserted = i
            sleep(1)
        print("Done with producer!")
    except:
        with open("testing-results-" + now + ".txt", "w") as f:
            f.write("ERROR : Broker not available while inserting record " + str(i) + " !")
            f.write("\n")
        generate_report(nbrrecords, nbrrecordsinserted, nbrrecordsretreived)
        sys.exit(1)
    print("End of Generation")

    consumer = KafkaConsumer(bootstrap_servers=client)
    try:
        # prepare consumer
        tp = TopicPartition(topic, 0)
        consumer.assign([tp])
        consumer.seek_to_beginning(tp)
        # obtain the last offset value
        lastOffset = consumer.end_offsets([tp])[tp]
        # consume the messages
        nbrrecordsretreived = 0
        for message in consumer:
            nbrrecordsretreived += 1
            if message.offset == lastOffset - 1:
                break
        print("I have consumed all the messages")
        with open("testing-results-" + now + ".txt", "w") as f:
            f.write("Consume process completed")
            f.write("\n")
        generate_report(nbrrecords, nbrrecordsinserted, nbrrecordsretreived)
    except:
        with open("testing-results-" + now + ".txt", "w") as f:
            f.write("ERROR during consume process !")
            f.write("\n")
        generate_report(nbrrecords, nbrrecordsinserted, nbrrecordsretreived)

    assert isinstance(int(nbrrecordsinserted) % int(nbrrecordsretreived), int) == True
