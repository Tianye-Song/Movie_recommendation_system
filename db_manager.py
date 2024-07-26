import mongodb.db as db
from data_quality.db_quality_check import *
import APIs.query as query
import json
import pandas as pd

IP = "128.2.204.215:8080"
VIRTUAL = "128.2.205.106:8082"


def query_user_info(user_id):
    user = query.getuser(IP, user_id)
    return user


def insert_new_entry(json_message):

    message = json.loads(json_message)
    if "time" in message.keys():
        db.insert_view_history(message)
        try:
            movie = query.getmovie(IP, message["movie_id"])
            db.insert_movie(message["movie_id"], movie)
        except Exception:
            pass
        try:
            user = query.getuser(IP, message["user_id"])
            db.insert_user(message["user_id"], user)
        except Exception:
            pass

    if "rating" in message.keys():
        db.insert_rate(message)
        try:
            movie = query.getmovie(IP, message["movie_id"])
            db.insert_movie(movie)
        except Exception:
            pass
        try:
            user = query.getuser(IP, message["user_id"])
            db.insert_user(user)
        except Exception:
            pass

    if "recommendations" in message.keys():
        db.insert_recommend_history(message)


def get_user(user_id):
    user = db.get_user(user_id)
    # if not user:
    #     user = query_user_info(user_id)
    #     db.insert_user(user_id, user)

    return user


def get_movie(movie_id):
    return db.get_movie(movie_id)


def get_movies(n):
    return db.get_movies(n)


def get_movies_df(n=0, query={}, projection={}):
    movies = db.get_movies(n, query, projection)
    # check data quality for the movies records
    results = []
    for m in movies:
        results.append(check_movies(m))
    return pd.DataFrame(results)


def get_users_df(n=0, query={}, projection={}):
    users = db.get_users(n, query, projection)
    # check data quality for the users records
    results = []
    for u in users:
        results.append(check_users(u))
    return pd.DataFrame(results)


def get_rates_df(n=0, query={}, projection={}):
    rates = db.get_rates(n, query, projection)
    # check data quality for the rates records
    results = []
    for r in rates:
        results.append(check_rates(r))
    return pd.DataFrame(results)


def get_rates_df_latest(datelist):
    results = []
    for date in datelist:
        # print("Start dates ", date)
        rates = db.get_rates_latest(date)
        for r in rates:
            results.append(check_rates(r))
        # print("results now have ", len(results))
    return pd.DataFrame(results)


def get_movies(n):
    return db.get_movies(n)


def get_rates(user_id):
    return db.get_rates(user_id)


def get_views(n):
    return db.get_views(n)


def insert_recommendation(user_id, recommendation):
    db.insert_recommendation(user_id, recommendation)


def insert_recommendation_m1(user_id, recommendation):
    db.insert_recommendation_m1(user_id, recommendation)


def insert_recommendation_m2(user_id, recommendation):
    db.insert_recommendation_m2(user_id, recommendation)


def get_recommendations(n=0, query={}, projection={}):
    recs = db.get_recommendations(n, query, projection)
    recommendations = {}
    for user in recs:
        recommendations[user["user_id"]] = user["movies"]

    return recommendations


def get_recommendations2(model_name, n=0, query={}, projection={}):
    recs = db.get_recommendations2(model_name, n, query, projection)
    recommendations = {}
    for user in recs:
        recommendations[user["user_id"]] = user["movies"]

    return recommendations


def get_history(date):
    history = db.get_recommendation_history(date)
    return pd.DataFrame(history)
