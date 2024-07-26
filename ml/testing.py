import sys
sys.path.append('..')
import mongodb.db as db
import pandas as pd
from data import get_data
from preprocess import clean
from db_manager import get_history, get_movies_df, get_users_df, get_rates_df, get_rates_df_latest
from KNN_recommendation import readJson
from datetime import datetime, date, timedelta
import csv
import time
import re
import os

def get_statistic(records, history):
    total_records_count = 0
    total_recommendation_count = 0
    num_correct = 0
    total_rates = 0
    top_rates = 0
    top_count = 0
    num_users = 0
    num_correct_users = 0
    for user, movies in history:
        num_users += 1
        if user not in records: # The user does not have any watching records.
            continue
        total_records_count += len(records[user]) # Count how many movie records.
        total_recommendation_count += len(movies) # Count how many movie recommendations.
        correctness = False
        for movie in list(records[user].keys()):
            if movie in movies: # The user has watched a movie on the recommendation list.
                correctness = True
                num_correct += 1 # Count how many recommended movies the user has watched.
                total_rates += records[user][movie] #Count the total rates.
                if movie == movies[0]: # Count the top recommendation movie
                    top_rates += records[user][movie] # The rates of the top recommended movie.
                    top_count += 1 # Count how any top recommended movies the user has watched.
        if correctness:
            num_correct_users += 1
    record_accuracy = num_correct / total_records_count
    record_accuracy = float("{0:.4f}".format(record_accuracy))
    recommendation_accuracy = num_correct_users / num_users
    recommendation_accuracy = float("{0:.4f}".format(recommendation_accuracy))
    avg_rates = total_rates / num_correct
    avg_rates = float("{0:.4f}".format(avg_rates))
    avg_top_rates = top_rates / top_count
    avg_top_rates = float("{0:.4f}".format(avg_top_rates))
    return num_correct_users, num_users, total_records_count, total_recommendation_count, num_correct, record_accuracy, recommendation_accuracy, total_rates, avg_rates, top_rates, top_count, avg_top_rates

def split_history(date):
    history = get_history(date)[['user_id', 'recommendations', 'models']]
    model_names = []
    model_history = {}
    for userid, recommendation, models in history:
        if model not in model_history:
            model_history[model] = []
            model_names.append(model)
        model_history[model].append((userid, recommendation))
    return model_names, model_history

def collect_rating_records(ratings):
    records = {}
    for index,row in ratings.iterrows():
        user = str(int(row['user_id']))
        movie = row['movie_id']
        score = row['rating']
        time = row['time_read']
        if user not in records:
            records[user] = {}
        records[user][movie] = score
    return records

'''
def ABtesting(date):
    movies, users, ratings = get_data()
    rating_records = collect_rating_records(ratings)
    model_names, model_history = split_history(date)
    first_column = ["Correct Recommendations", "Total Records", "Record Accuracy", "Correct Recommendation Users", "Total Users", "Recommendation Accuracy", "Average Rating", "Top Correct Recommendation", "Average Top Rating"]
    result_dict = {}
    result_dict["Attributes"] = first_column
    for model in model_names:
        history = model_history[model]
        num_correct_users, num_users, total_records_count, total_recommendation_count, num_correct, record_accuracy, recommendation_accuracy, total_rates, avg_rates, top_rates, top_count, avg_top_rates = get_statistic(records, rating_records)
    first_column = ["Attributes", "Correct Recommendations", "Total Records", "Record Accuracy", "Correct Recommendation Users", "Total Users", "Recommendation Accuracy", "Average Rating", "Top Correct Recommendation", "Average Top Rating"]
    temp = [model, num_correct, total_records_count, record_accuracy, num_correct_users, num_users, recommendation_accuracy, avg_rates, top_count, avg_top_rates]
        temp = [num_correct, total_records_count, record_accuracy, num_correct_users, num_users, recommendation_accuracy, avg_rates, top_count, avg_top_rates]
'''

def ABtesting(date, timestamp):
    start_time = time.time()
    print("> Start AB testing....")
    ratings = get_rates_df()
    ratings = clean(ratings)
    rating_records = collect_rating_records(ratings)
    history = get_history(date)[['user_id', 'recommendations']].to_numpy().tolist()
    print("> Loading data finished, the time is ", time.time() - start_time)
    print("> Start Evaluating....")
    start_time = time.time()
    first_column = ["Correct Recommendations", "Total Records", "Record Accuracy", "Correct Recommendation Users", "Total Users", "Recommendation Accuracy", "Average Rating", "Top Correct Recommendation", "Average Top Rating"]
    result_dict = {}
    result_dict["Attributes"] = first_column
    #for model in model_names:
        #history = model_history[model]
    num_correct_users, num_users, total_records_count, total_recommendation_count, num_correct, record_accuracy, recommendation_accuracy, total_rates, avg_rates, top_rates, top_count, avg_top_rates = get_statistic(rating_records, history)
    temp = [num_correct, total_records_count, record_accuracy, num_correct_users, num_users, recommendation_accuracy, avg_rates, top_count, avg_top_rates]
    result_dict["KNN"] = temp
    output = pd.DataFrame(result_dict, columns = ["Attributes", "KNN"])
    output.to_csv("Eval" + timestamp + ".csv", index=False)
    print("> Evaluatig finished Write to csv Eval" + timestamp + ".csv, time is " + str(time.time() - start_time))

def randomABtesting(date, timestamp, dir1, dir2):
    start_time = time.time()
    print("> Start AB testing....")
    ratings = get_rates_df()
    ratings = clean(ratings)
    rating_records = collect_rating_records(ratings)
    history = get_history(date)['user_id'].to_numpy().tolist()
    recommendation1 = readJson("./" + dir1 + "/recommendation_result.json")
    recommendation2 = readJson("./" + dir2 + "/recommendation_result.json")
    his1 = []
    his2 = []
    for userid in history:
        user_id = re.sub("[^0-9]", "", userid)
        if int(user_id[0]) % 2 == 0:
            temp = recommendation1[userid] if userid in recommendation1 else recommendation1['NA']
            his1.append([userid, temp])
        else:
            temp = recommendation2[userid] if userid in recommendation2 else recommendation2['NA']
            his2.append([userid, temp])
    print("len(his1) is ", len(his1))
    print("len(his2) is ", len(his2))
    print("> Loading data finished, the time is ", time.time() - start_time)
    print("> Start Evaluating....")
    start_time = time.time()
    first_column = ["Correct Recommendations", "Total Records", "Record Accuracy", "Correct Recommendation Users", "Total Users", "Recommendation Accuracy", "Average Rating", "Top Correct Recommendation", "Average Top Rating"]
    result_dict = {}
    result_dict["Attributes"] = first_column
    #for model in model_names:
        #history = model_history[model]
    num_correct_users, num_users, total_records_count, total_recommendation_count, num_correct, record_accuracy, recommendation_accuracy, total_rates, avg_rates, top_rates, top_count, avg_top_rates = get_statistic(rating_records, his1)
    temp = [num_correct, total_records_count, record_accuracy, num_correct_users, num_users, recommendation_accuracy, avg_rates, top_count, avg_top_rates]
    result_dict[dir1] = temp
    num_correct_users, num_users, total_records_count, total_recommendation_count, num_correct, record_accuracy, recommendation_accuracy, total_rates, avg_rates, top_rates, top_count, avg_top_rates = get_statistic(rating_records, his2)
    temp = [num_correct, total_records_count, record_accuracy, num_correct_users, num_users, recommendation_accuracy, avg_rates, top_count, avg_top_rates]
    result_dict[dir2] = temp
    output = pd.DataFrame(result_dict, columns = ["Attributes", dir1, dir2])
    output.to_csv("./Online0413/Eval" + timestamp + ".csv", index=False)
    print("> Evaluatig finished Write to csv Eval" + timestamp + ".csv, time is " + str(time.time() - start_time))

if __name__ == "__main__":
    mydate = date.today().strftime("%Y-%m-%d")
    mytime = datetime.now().strftime("%Y-%m-%d-%H-%M")
    if not os.path.isdir("./Online0413"):
        os.mkdir("./Online0413/")
    dir1 = "KNN2022-04-08"
    dir2 = "KNN2022-04-12"
    #dir1 and dir2 are two folder names where you read recommendation_result.json.
    #.pyrandomABtesting("2022-04-12", mytime, dir1, dir2)
    while True:
        mytime = datetime.now().strftime("%Y-%m-%d-%H-%M")
        #ABtesting(mydate, mytime)
        randomABtesting(mydate, mytime, dir1, dir2)
        time.sleep(3600)