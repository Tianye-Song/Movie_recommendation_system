import sys
sys.path.append('..')
import mongodb.db as db
import pandas as pd
import numpy as np
from data import get_data, get_latest_data
from preprocess import clean, collect_rating_records
from db_manager import get_history, get_movies_df, get_users_df, get_rates_df, get_rates_df_latest
from online_evaluation import get_user_dict
from KNN_recommendation import readJson
from datetime import datetime, date, timedelta

def collect_user_dict():
    users = get_users_df()
    user_dict = get_user_dict(users)
    return user_dict
        

def get_record_dict(start, end):
    movies, original_ratings = get_latest_data(start, end)
    ratings = clean(original_ratings)
    record_dict = collect_rating_records(ratings)
    return record_dict

def detect_average_rate():
    my_date = date.today()
    times = [(my_date - timedelta(days=N)).strftime("%Y-%m-%d") for N in range(4, 18)]
    for day in times:
        print("The date is ", day)
        rates_df = get_rates_df_latest([day])
        ratings = rates_df[["rating"]]
        print(ratings.describe())
        print('===========================')


def examine_exist(recommendation, day):
    history = get_history(day)['user_id'].to_numpy().tolist()
    print("The number of users request is ", len(history))
    exist = 0
    for userid in history:
        if userid in recommendation:
            exist += 1
    print("The number of exist is ", exist)

def population_telemetry(user_dict, record_dict, recommendation_dict):
    user_list = list(record_dict.keys())
    #First we perform gender population evaluation
    gender_result = {}
    gender_result = telemetry_eval('gender', user_dict, user_list, record_dict, recommendation_dict, gender_result)
    for key in list(gender_result.keys()):
        gender_result[key]["record_accuracy"] = gender_result[key]["correct_recommendations"] / gender_result[key]["total_records_count"]
        gender_result[key]['recommendation_accuracy'] = gender_result[key]["correct_users"] / gender_result[key]["num_users"]
        gender_result[key]["avg_rates"] = gender_result[key]["total_rates"] / gender_result[key]["correct_recommendations"]
        gender_result[key]["avg_top_rates"] = gender_result[key]["top_rates"] / gender_result[key]["top_count"]
    #Then we perform gender occupation evaluation
    occupation_result = {}
    occupation_result = telemetry_eval('occupation', user_dict, user_list, record_dict, recommendation_dict, occupation_result)
    for key in list(occupation_result.keys()):
        occupation_result[key]["record_accuracy"] = occupation_result[key]["correct_recommendations"] / occupation_result[key]["total_records_count"]
        occupation_result[key]['recommendation_accuracy'] = occupation_result[key]["correct_users"] / occupation_result[key]["num_users"]
        occupation_result[key]["avg_rates"] = occupation_result[key]["total_rates"] / occupation_result[key]["correct_recommendations"]
        occupation_result[key]["avg_top_rates"] = occupation_result[key]["top_rates"] / occupation_result[key]["top_count"]
     #Then we perform gender Age evaluation
    Age_result = {}
    Age_result = telemetry_eval('Age', user_dict, user_list, record_dict, recommendation_dict, Age_result)
    for key in list(Age_result.keys()):
        Age_result[key]["record_accuracy"] = Age_result[key]["correct_recommendations"] / Age_result[key]["total_records_count"]
        Age_result[key]['recommendation_accuracy'] = Age_result[key]["correct_users"] / Age_result[key]["num_users"]
        Age_result[key]["avg_rates"] = Age_result[key]["total_rates"] / Age_result[key]["correct_recommendations"]
        Age_result[key]["avg_top_rates"] = Age_result[key]["top_rates"] / Age_result[key]["top_count"]
    return gender_result, occupation_result, Age_result



def telemetry_eval(attribute, user_dict, user_list, records, recommendation_dict, result):
    for user in user_list:
        if user not in user_dict or user not in records:
            continue
        #print("Start eval user ", user)
        key = user_dict[user][attribute]
        if key not in result:
            result[key] = {"num_users": 0, "total_records_count": 0, "correct_recommendations": 0, 
                            "correct_users": 0, "record_accuracy": 0, "recommendation_accuracy": 0,
                            "total_rates": 0, "avg_rates": 0, "top_rates": 0, "top_count": 0, "avg_top_rates": 0}
        result[key]["num_users"] += 1
        result[key]["total_records_count"] += len(records[user]) # Count how many movie records.
        correctness = False
        movies = recommendation_dict[user] if user in recommendation_dict else recommendation_dict['NA']
        for movie in list(records[user].keys()):
            if movie in movies: # The user has watched a movie on the recommendation list.
                correctness = True
                result[key]["correct_recommendations"] += 1
                result[key]["total_rates"] += records[user][movie] #Count the total rates.
                if movie == movies[0]: # Count the top recommendation movie
                    result[key]["top_rates"] += records[user][movie]
                    result[key]["top_count"] += 1 # Count how any top recommended movies the user has watched.
        if correctness:
            result[key]["correct_users"] += 1
    return result

if __name__ == "__main__":
    user_dict = collect_user_dict()
    record_dict = get_record_dict(1, 29)
    print("record_dict is ", list(record_dict.keys())[:20])
    recommendation_dict = readJson("./KNN2022-04-14/recommendation_result.json")
    gender_result, occupation_result, Age_result = population_telemetry(user_dict, record_dict, recommendation_dict)
    print("Start presenting gender evaluation result:")
    print(gender_result)
    print("-----------------")
    print("Start presenting occupation evaluation result:")
    print(occupation_result)
    print('-----------------')
    print("Start presenting age evaluation result:")
    print(Age_result)
