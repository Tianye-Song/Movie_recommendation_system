import os
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from pymongo import MongoClient
from surprise import Reader, Dataset, KNNWithMeans, dump
from surprise.model_selection import train_test_split, cross_validate, GridSearchCV
import sys
import json
import time
import pickle

sys.path.append("..")
from surprise.accuracy import rmse, mse, mae

# sys.path.append("..")
# sys.path.append("/home/lfgomes/group-project-s22-dsu/ml/")
# from surprise.accuracy import rmse, mse, mae
from data import get_data, get_latest_data
from preprocess import (
    clean,
    map_movies,
    map_users,
    get_rating_users,
    get_rating_movies,
    get_top_50_popular_movies,
)
from db_manager import insert_recommendation_m1, insert_recommendation_m2


def offline_evaluation(algo, trainset, testset):
    print("> Start offline evaluation...")
    start_time = time.time()
    algo.fit(trainset)
    print("The model training time is ", time.time() - start_time)
    # filename = 'KNN.sav'
    # pickle.dump(algo, open(filename, 'wb'))
    start_time = time.time()
    predictions = algo.test(testset)
    print("The offline evaluation RMSE is ", rmse(predictions))
    print("The offline evaluation MSE is ", mse(predictions))
    print("The offline evaluation MAE is ", mae(predictions))
    print("The model prediction time is ", time.time() - start_time)
    return algo


def save_data(data, filename):
    with open(filename, "w") as fp:
        json.dump(data, fp)


def KNN_train(
    ratings,
    filter_users,
    filter_movies,
    user_id_dict_reversed,
    movie_id_dict_reversed,
    model_filename,
    data_filename,
    verbose=True,
):
    start = time.time()

    print("> Process the data...")
    df_new = ratings[
        (ratings["movie_id"].isin(filter_movies))
        & (ratings["user_id"].isin(filter_users))
    ]
    df_new["user_id"] = df_new["user_id"].map(user_id_dict_reversed)
    df_new["movie_id"] = df_new["movie_id"].map(movie_id_dict_reversed)
    print("The original data frame shape:\t{}".format(ratings.shape))
    print("The new data frame shape:\t{}".format(df_new.shape))
    print("> OK")
    print("It took " + str(time.time() - start) + " seconds")

    start = time.time()
    print("> Loading data...")
    reader = Reader(rating_scale=(1, 5))
    if df_new.shape[0] > 30000:
        print("Too many data, needs to clip to 30,000!")
        df_new = df_new[:30000]
    df_new.to_csv(data_filename, index=False)
    rating_data = Dataset.load_from_df(
        df_new[["user_id", "movie_id", "rating"]], reader
    )
    trainset, testset = train_test_split(
        rating_data, test_size=0.2, shuffle=False
    )
    print("> OK")
    print("It took " + str(time.time() - start) + " seconds")

    start = time.time()
    param_grid = {
        "k": 30,
        "bsl_options": {"method": "als", "n_epochs": 1, "reg_u": 10, "reg_i": 20},
        "sim_options": {"name": "pearson_baseline", "user_based": False},
    }
    model = KNNWithMeans(
        k=param_grid["k"],
        bsl_options=param_grid["bsl_options"],
        sim_options=param_grid["sim_options"],
    )
    model = offline_evaluation(model, trainset, testset)
    start = time.time()
    # model_filename = "./KNN.pickle"
    print(">> Starting dump")
    # Dump algorithm and reload it.
    file_name = os.path.expanduser(model_filename)
    dump.dump(file_name, algo=model)

    print(">> Dump done")
    print("It took " + str(time.time() - start) + " seconds")
    return df_new


def pipeline(startday, endday, min_users_rating, min_movies_rating, directory):
    print("\n\n\t\t STARTING\n\n")
    start = time.time()
    print("> Loading data...")
    model_filename = directory + "model.pickle"
    data_filename = directory + "data.json"
    csv_filename = directory + "ratings.csv"
    # The pipeline is used as this: It will collect the date from today's date - (endday - 1) to today's date - (startday).
    # For instance, assume today is Apr 11, startday = 0, endday = 4, it will get Apr 8, Apr 9, Apr 10, Apr 11.
    movies, original_ratings = get_latest_data(startday, endday)
    ratings = clean(original_ratings)
    movie_id_dict, movie_id_dict_reversed = map_movies(ratings)
    user_id_dict, user_id_dict_reversed = map_users(ratings)
    rating_users = get_rating_users(ratings, min_users_rating)
    rating_movies = get_rating_movies(ratings, min_movies_rating)
    top_50_popular_movies = get_top_50_popular_movies(movies)
    result_data = {}
    # result_data["training_data"] = df_new
    result_data["top_50_popular_movies"] = top_50_popular_movies
    result_data["rating_users"] = rating_users
    result_data["rating_movies"] = rating_movies
    result_data["user_id_dict"] = user_id_dict
    result_data["user_id_dict_reversed"] = user_id_dict_reversed
    result_data["movie_id_dict"] = movie_id_dict
    result_data["movie_id_dict_reversed"] = movie_id_dict_reversed
    save_data(result_data, data_filename)
    print("> OK")
    print("It took " + str(time.time() - start) + " seconds")
    KNN_train(
        ratings,
        rating_users,
        rating_movies,
        user_id_dict_reversed,
        movie_id_dict_reversed,
        model_filename,
        csv_filename,
    )


if __name__ == "__main__":
    min_users_rating = 1  # int(sys.argv[1])
    min_movies_rating = 1  # int(sys.argv[2])
    pipeline(0, 7, min_users_rating, min_movies_rating, "KNN0411")
