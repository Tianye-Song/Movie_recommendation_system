from random import random
import sys

sys.path.append("/home/lfgomes/group-project-s22-dsu")

import random
from datetime import date, timedelta
from surprise import dump
from db_manager import insert_recommendation_m1, insert_recommendation_m2

import os
from data import get_data
from preprocess import (
    clean,
    collect_rating_records,
    map_movies,
    map_users,
    get_rating_users,
    get_rating_movies,
    get_top_50_popular_movies,
)

from KNN import offline_evaluation, KNN_train, pipeline
import time
import json

## LOAD SAVED MODEL
def load_model(model_filename):
    print(">> Loading dump")
    file_name = os.path.expanduser(model_filename)
    _, loaded_model = dump.load(file_name)
    print(">> Loaded dump")
    return loaded_model


def recommendation(algo, userid, rating_users, rating_movies, top_50_popular_movies):
    if userid not in rating_users:
        return top_50_popular_movies
    prediction = [(i, algo.predict(userid, i).est) for i in rating_movies]
    prediction.sort(key=lambda x: x[1], reverse=True)
    result = [item[0] for item in prediction[:50]]
    return result


def get_recommendation(
    algo, user_id_dict_reversed, rating_users, rating_movies, top_50_popular_movies
):
    result_dict = {}
    result_dict["NA"] = top_50_popular_movies
    NA_jsons = {"user_id": "NA", "movies": top_50_popular_movies}
    # insert_recommendation('NA', NA_jsons)
    for userid in rating_users:
        userid = user_id_dict_reversed[str(int(userid))]
        result = recommendation(
            algo, userid, rating_users, rating_movies, top_50_popular_movies
        )
        jsons = {"user_id": userid, "movies": result}
        # insert_recommendation(userid, jsons)
        result_dict[userid] = result
    return result_dict


def writeJson(data, filename):
    jsons = json.dumps(data)
    f = open(filename, "w")
    f.write(jsons)
    f.close()


def readJson(filename):
    f = open(filename)
    data = json.load(f)
    return data


def recommend(model_label, startday, endday, min_users_rating=0, min_movies_rating=0):
    # The pipeline is used as this: It will collect the date from today's date - (endday - 1) to today's date - (startday).
    # For instance, assume today is Apr 11, startday = 0, endday = 4, it will get Apr 8, Apr 9, Apr 10, Apr 11.
    my_date = date.today()
    directory = (
        "/home/lfgomes/group-project-s22-dsu/KNN_"
        + str(model_label)
        + "_"
        + str(my_date)
        + "/"
    )
    print("Directory:", directory)
    if not os.path.isdir(directory):
        os.mkdir(directory)
    model_filename = directory + "model.pickle"
    data_filename = directory + "data.json"
    recommendation_result_filename = directory + "recommendation_result.json"
    pipeline(0, 5, min_users_rating, min_movies_rating, directory)
    model = load_model(model_filename)
    f = open(data_filename)
    data = json.load(f)
    rating_users = data["rating_users"]
    rating_movies = data["rating_movies"]
    user_id_dict_reversed = data["user_id_dict_reversed"]
    top_50_popular_movies = data["top_50_popular_movies"]
    rating_users_set = set(rating_users)
    rating_movies_set = set(rating_movies)
    recommendation_dict = get_recommendation(
        model,
        user_id_dict_reversed,
        rating_users_set,
        rating_movies_set,
        top_50_popular_movies,
    )

    if model_label == 1:
        for key, value in recommendation_dict.items():
            recommendation = {"user_id": str(key), "movies": value}
            insert_recommendation_m1(key, recommendation)
    elif model_label == 2:
        for key, value in recommendation_dict.items():
            recommendation = {"user_id": str(key), "movies": value}
            insert_recommendation_m2(key, recommendation)

    writeJson(recommendation_dict, recommendation_result_filename)


if __name__ == "__main__":
    min_users_rating = 0  # int(sys.argv[1])
    min_movies_rating = 0  # int(sys.argv[2])
    model = int(sys.argv[1])
    if model == 1:
        # Train data from Apr 7 to Apr 11, and save in the folder "KNN2022-04-11"
        recommend(model, 0, 5, min_users_rating=0, min_movies_rating=0)
    else:
        # Train data from Apr 6 to Apr 10, and save in the folder "KNN2022-04-10"
        recommend(model, 1, 6, min_users_rating=0, min_movies_rating=0)
