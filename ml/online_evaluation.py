import sys
sys.path.append('..')
import mongodb.db as db
import pandas as pd
from db_manager import get_history, get_movies_df, get_users_df, get_rates_df, get_rates_df_latest
from KNN_recommendation import readJson
from datetime import date, timedelta
import csv
#Get the statistic from the true watching records and recommendation history.
def get_attribute_statistic(records, history, attribute, value, userdict):
    total_records_count = 0
    total_recommendation_count = 0
    num_correct = 0
    total_rates = 0
    top_rates = 0
    top_count = 0
    num_users = 0
    num_correct_users = 0
    for user, movies in history:
        if user not in userdict or userdict[user][attribute] != value:
            continue
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

def evaluate_attribute(dates, records, attribute, value, userdict):
    _num_correct_users = _num_users = _total_records_count = _total_recommendation_count = _num_correct = \
        _total_rates = _top_rates = _top_count = 0
    num_correct_users_list = []
    num_users_list = []
    total_records_count_list = []
    total_recommendation_count_list = []
    num_correct_list = []
    top_count_list = []
    record_accuracy_list = []
    recommendation_accuracy_list = []
    avg_rates_list = []
    avg_top_rates_list = []
    result = []
    for date in dates:
        print(">Start online evaluation on ", date)
        history = get_history(date)[['user_id', 'recommendations']]
        history = history.to_numpy().tolist()
        num_correct_users, num_users, total_records_count, total_recommendation_count, num_correct, \
            record_accuracy, recommendation_accuracy, total_rates, \
            avg_rates, top_rates, top_count, avg_top_rates = get_attribute_statistic(records, history, attribute, value, userdict)
        print("The number of users we evaluate: ", num_users)
        print("The number of users who watches the top recommended movie is ", top_count)
        print("The ratio of recommendation the users have watched is {:.2%}".format(record_accuracy))
        print("The ratio of movies the users have watched occurs on our recommendation is {:.2%}".format(recommendation_accuracy))
        print("The avergae rating for our recommendation is {0:.4}".format(avg_rates))
        print("The avergae rating for our top recommendation is {0:.4}".format(avg_top_rates))
        record_accuracy_list.append(record_accuracy)
        recommendation_accuracy_list.append(recommendation_accuracy)
        avg_rates_list.append(avg_rates)
        avg_top_rates_list.append(avg_top_rates)
        num_correct_users_list.append(num_correct_users)
        _num_correct_users += num_correct_users
        num_users_list.append(num_users)
        _num_users += num_users
        total_records_count_list.append(total_records_count)
        _total_records_count += total_records_count
        total_recommendation_count_list.append(total_recommendation_count)
        _total_recommendation_count += total_recommendation_count
        num_correct_list.append(num_correct)
        _num_correct += num_correct
        _total_rates +=  total_rates
        _top_rates += top_rates
        top_count_list.append(top_count)
        _top_count += top_count
        temp = [num_correct, total_records_count, num_correct_users, num_users,
            record_accuracy, recommendation_accuracy, avg_rates, top_count, avg_top_rates]
        result.append(temp)
    if len(dates) > 1:
        _record_accuracy = _num_correct / _total_records_count
        _record_accuracy = float("{0:.4f}".format(_record_accuracy))
        _recommendation_accuracy = _num_correct_users / _num_users
        _recommendation_accuracy = float("{0:.4f}".format(_recommendation_accuracy))
        _avg_rates = _total_rates / _num_correct
        _avg_rates = float("{0:.4f}".format(_avg_rates))
        _avg_top_rates = _top_rates / _top_count
        _avg_top_rates = float("{0:.4f}".format(_avg_top_rates))
        record_accuracy_list.append(_record_accuracy)
        recommendation_accuracy_list.append(_recommendation_accuracy)
        avg_rates_list.append(_avg_rates)
        avg_top_rates_list.append(_avg_top_rates)
        num_users_list.append(_num_users)
        total_records_count_list.append(_total_records_count)
        total_recommendation_count_list.append(_total_recommendation_count)
        num_correct_list.append(_num_correct)
        top_count_list.append(_top_count)
        temp = [_num_correct, _total_records_count, _num_correct_users, _num_users,
            _record_accuracy, _recommendation_accuracy, _avg_rates, _top_count, _avg_top_rates]
        result.append(temp)
        print("====================")
        print(">Summary:")
        print("The number of users we evaluate: ", _num_users)
        print("The number of users who watches the top recommended movie is ", _top_count)
        print("The ratio of recommendation the users have watched is {:.2%}".format(_record_accuracy))
        print("The ratio of movies the users have watched occurs on our recommendation is {:.2%}".format(_recommendation_accuracy))
        print("The avergae rating for our recommendation is {0:.4}".format(_avg_rates))
        print("The avergae rating for our top recommendation is {0:.4}".format(_avg_top_rates))
        #return num_users_list, total_records_count_list, total_recommendation_count_list, \
        #        num_correct_list, top_count_list, record_accuracy_list, \
        #        recommendation_accuracy_list, avg_rates_list, avg_top_rates_list
        
        return result



def evaluate(dates, records):
    _num_correct_users = _num_users = _total_records_count = _total_recommendation_count = _num_correct = \
        _total_rates = _top_rates = _top_count = 0
    num_correct_users_list = []
    num_users_list = []
    total_records_count_list = []
    total_recommendation_count_list = []
    num_correct_list = []
    top_count_list = []
    record_accuracy_list = []
    recommendation_accuracy_list = []
    avg_rates_list = []
    avg_top_rates_list = []
    result = []
    for date in dates:
        print(">Start online evaluation on ", date)
        history = get_history(date)[['user_id', 'recommendations']]
        history = history.to_numpy().tolist()
        num_correct_users, num_users, total_records_count, total_recommendation_count, num_correct, \
            record_accuracy, recommendation_accuracy, total_rates, \
            avg_rates, top_rates, top_count, avg_top_rates = get_statistic(records, history)
        print("The number of users we evaluate: ", num_users)
        print("The number of users who watches the top recommended movie is ", top_count)
        print("The ratio of recommendation the users have watched is {:.2%}".format(record_accuracy))
        print("The ratio of movies the users have watched occurs on our recommendation is {:.2%}".format(recommendation_accuracy))
        print("The avergae rating for our recommendation is {0:.4}".format(avg_rates))
        print("The avergae rating for our top recommendation is {0:.4}".format(avg_top_rates))
        record_accuracy_list.append(record_accuracy)
        recommendation_accuracy_list.append(recommendation_accuracy)
        avg_rates_list.append(avg_rates)
        avg_top_rates_list.append(avg_top_rates)
        num_correct_users_list.append(num_correct_users)
        _num_correct_users += num_correct_users
        num_users_list.append(num_users)
        _num_users += num_users
        total_records_count_list.append(total_records_count)
        _total_records_count += total_records_count
        total_recommendation_count_list.append(total_recommendation_count)
        _total_recommendation_count += total_recommendation_count
        num_correct_list.append(num_correct)
        _num_correct += num_correct
        _total_rates +=  total_rates
        _top_rates += top_rates
        top_count_list.append(top_count)
        _top_count += top_count
        temp = [num_correct, total_records_count, num_correct_users, num_users,
            record_accuracy, recommendation_accuracy, avg_rates, top_count, avg_top_rates]
        result.append(temp)
    if len(dates) > 1:
        _record_accuracy = _num_correct / _total_records_count
        _record_accuracy = float("{0:.4f}".format(_record_accuracy))
        _recommendation_accuracy = _num_correct_users / _num_users
        _recommendation_accuracy = float("{0:.4f}".format(_recommendation_accuracy))
        _avg_rates = _total_rates / _num_correct
        _avg_rates = float("{0:.4f}".format(_avg_rates))
        _avg_top_rates = _top_rates / _top_count
        _avg_top_rates = float("{0:.4f}".format(_avg_top_rates))
        record_accuracy_list.append(_record_accuracy)
        recommendation_accuracy_list.append(_recommendation_accuracy)
        avg_rates_list.append(_avg_rates)
        avg_top_rates_list.append(_avg_top_rates)
        num_users_list.append(_num_users)
        total_records_count_list.append(_total_records_count)
        total_recommendation_count_list.append(_total_recommendation_count)
        num_correct_list.append(_num_correct)
        top_count_list.append(_top_count)
        temp = [_num_correct, _total_records_count, _num_correct_users, _num_users,
            _record_accuracy, _recommendation_accuracy, _avg_rates, _top_count, _avg_top_rates]
        result.append(temp)
        print("====================")
        print(">Summary:")
        print("The number of users we evaluate: ", _num_users)
        print("The number of users who watches the top recommended movie is ", _top_count)
        print("The ratio of recommendation the users have watched is {:.2%}".format(_record_accuracy))
        print("The ratio of movies the users have watched occurs on our recommendation is {:.2%}".format(_recommendation_accuracy))
        print("The avergae rating for our recommendation is {0:.4}".format(_avg_rates))
        print("The avergae rating for our top recommendation is {0:.4}".format(_avg_top_rates))
        #return num_users_list, total_records_count_list, total_recommendation_count_list, \
        #        num_correct_list, top_count_list, record_accuracy_list, \
        #        recommendation_accuracy_list, avg_rates_list, avg_top_rates_list
        
        return result
    
# Get the date of today.
def get_latest_day():
    return [date.today().strftime("%Y-%m-%d")]

# Get the dates of the latest week.
def get_latest_week():
    my_date = date.today()
    return [(my_date - timedelta(days=N)).strftime("%Y-%m-%d") for N in range(1, 8)]

# Get the dates of the latest months
def get_latest_month():
    my_date = date.today()
    return [(my_date - timedelta(days=N)).strftime("%Y-%m-%d") for N in range(30)]

def get_user_dict(users):
    userids = users["user_id"].tolist()
    genders = users["gender"].tolist()
    occupations = users["occupation"].tolist()
    ages = users["age"].tolist()
    user_dict = {}
    for id, gender, occupation, age in zip(userids, genders, occupations, ages):
        Age = None
        if age < 20:
            Age = "Teenager"
        elif age < 30:
            Age = "Adult"
        elif age < 50:
            Age = "Senior"
        else:
            Age = "Elder"
        user_dict[str(id)] = {"gender": gender, "occupation": occupation, "Age": Age}
    return user_dict


if __name__ == "__main__":
    users = get_users_df()
    user_dict = get_user_dict(users)
    records = readJson("ratings_record.json")  
    M_result = evaluate_attribute(get_latest_week(), records, "gender", "M", user_dict)
    F_result = evaluate_attribute(get_latest_week(), records, "gender", "F", user_dict)
    result = evaluate(get_latest_week(), records)
    export_data = list(zip(result))
    df = pd.DataFrame(result)
    df.to_csv('online_result_0331.csv', sep=' ', index = False)



