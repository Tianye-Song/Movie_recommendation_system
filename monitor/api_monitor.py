import sys
import time
from datetime import datetime
from prometheus_client import Counter, Histogram, start_http_server

sys.path.append("../data_quality")
sys.path.append("../mongodb")

from db_quality_check import *
from db import *

start_http_server(8764)

# Counter for request count
REQUEST_COUNT = Counter('request_count',
                        'Recommendation Request Count',
                        ['http_status'])

# Histogram for request latency distribution
REQUEST_LATENCY = Histogram('request_latency_seconds',
                            'Request_latency')

# Time format of time_read in mongodb
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def main():
    # Fetch and monitor data from mongodb every 60s 
    past_time = datetime.now().strftime(TIME_FORMAT)
    while True:
        current_time = datetime.now().strftime(TIME_FORMAT)
        messages = get_recommendation_history_between(past_time, current_time)
        messages = [trim_str_value(m) for m in messages]
        for m in messages:
            # Collect total request count data of different http status 
            REQUEST_COUNT.labels(m['status']).inc()
            # Collect request latency data to plot distribution in histogram 
            REQUEST_LATENCY.observe(int(m['response_time']) / 1000)
        time.sleep(60)
        past_time = current_time


if __name__ == "__main__":
    main()
