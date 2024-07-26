import re
import os
import time
import pandas as pd
from datetime import datetime, timedelta
from prometheus_client import Gauge, start_http_server

start_http_server(8763)

# Monitor online evaluation metrics
# Use Gauge to represents a single numerical value 
# that can arbitrarily go up and down
CORRECT_RECOM = Gauge('corrent_recommendation_count', 
                      'Correnct Recommendation Count',
                      ['model_version'])
TOTAL_RECORD = Gauge('records_count', 
                     'Total Records',
                     ['model_version'])
RECORD_ACCURACY = Gauge('record_accuracy_rate', 
                        'Record Accuracy',
                        ['model_version'])
CORRECT_RECOM_USERS = Gauge('correct_recommendation_users', 
                            'Correct Recommendation Users',
                            ['model_version'])
TOTAL_USERS = Gauge('user_count', 
                    'Total User Number Count',
                    ['model_version'])
RECOM_ACCURACY = Gauge('recommendation_accuracy_rate', 
                       'Recommendation Accuracy',
                       ['model_version'])
AVG_RATE = Gauge('average_rating', 
                 'Average Rating',
                 ['model_version'])
TOP_CORRECT_RECOM= Gauge('top_correct_recommendation', 
                         'Top Correct Recommendation',
                         ['model_version'])
AVG_TOP_RATE = Gauge('average_top_rating', 
                     'Average Top Rating',
                     ['model_version'])


ROOT_PATH = "/home/liangwez/group-project-s22-dsu/ml/Online0413"
MODEL_A = 'KNN2022-04-08'
MODEL_B = 'KNN2022-04-12'
TIME_FORMAT = "%Y-%m-%d-%H"


def main():
    while True:
        # Use the metric file of the past hour 
        # in case the metric file is not updated timely
        current_time = (datetime.now()- timedelta(hours=1)).strftime(TIME_FORMAT)
        for filename in os.listdir(ROOT_PATH):
            if re.search(current_time, filename):
                # Fetch data every 30mins 
                metric_path = os.path.join(ROOT_PATH, filename)
                metric_file = pd.read_csv(metric_path, index_col=0)
                # Collect online evaluation metric data 
                CORRECT_RECOM.labels(MODEL_A).set(metric_file.loc['Correct Recommendations', MODEL_A])
                CORRECT_RECOM.labels(MODEL_B).set(metric_file.loc['Correct Recommendations', MODEL_B])
                
                TOTAL_RECORD.labels(MODEL_A).set(metric_file.loc['Total Records',MODEL_A])
                TOTAL_RECORD.labels(MODEL_B).set(metric_file.loc['Total Records',MODEL_B])
                
                RECORD_ACCURACY.labels(MODEL_A).set(metric_file.loc['Record Accuracy',MODEL_A])
                RECORD_ACCURACY.labels(MODEL_B).set(metric_file.loc['Record Accuracy',MODEL_B])
                
                CORRECT_RECOM_USERS.labels(MODEL_A).set(metric_file.loc['Correct Recommendation Users',MODEL_A])
                CORRECT_RECOM_USERS.labels(MODEL_B).set(metric_file.loc['Correct Recommendation Users',MODEL_B])
                
                TOTAL_USERS.labels(MODEL_A).set(metric_file.loc['Total Users',MODEL_A])
                TOTAL_USERS.labels(MODEL_B).set(metric_file.loc['Total Users',MODEL_B])
                
                RECOM_ACCURACY.labels(MODEL_A).set(metric_file.loc['Recommendation Accuracy',MODEL_A])
                RECOM_ACCURACY.labels(MODEL_B).set(metric_file.loc['Recommendation Accuracy',MODEL_B])
                
                AVG_RATE.labels(MODEL_A).set(metric_file.loc['Average Rating',MODEL_A])
                AVG_RATE.labels(MODEL_B).set(metric_file.loc['Average Rating',MODEL_B])
                
                TOP_CORRECT_RECOM.labels(MODEL_A).set(metric_file.loc['Top Correct Recommendation',MODEL_A])
                TOP_CORRECT_RECOM.labels(MODEL_B).set(metric_file.loc['Top Correct Recommendation',MODEL_B])
                
                AVG_TOP_RATE.labels(MODEL_A).set(metric_file.loc['Average Top Rating',MODEL_A])
                AVG_TOP_RATE.labels(MODEL_B).set(metric_file.loc['Average Top Rating',MODEL_B])
                time.sleep(1800)
                break
        

if __name__ == "__main__":
    main()


