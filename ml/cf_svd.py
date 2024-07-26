import os
import pandas as pd
from pymongo import MongoClient
from surprise import Reader, Dataset, dump
from surprise.model_selection import train_test_split
import sys
import json
sys.path.append('..')
import time
from surprise.accuracy import rmse, mse, mae

from surprise import SVD
from surprise.model_selection import GridSearchCV

from db_manager import get_movies_df, get_users_df, get_rates_df
from data import get_data
from preprocess import clean, map_movies, map_users, get_rating_users, get_rating_movies, get_top_50_popular_movies

"""
def get_data():
    movies = get_movies_df()
    print("The number of movies we get is", movies.shape[0]) #25327
    users = get_users_df()
    print("The number of users we get is", users.shape[0]) #130369
    ratings = get_rates_df()
    print("The number of ratings we get is", ratings.shape[0]) #16351   
    return movies, users, ratings
"""
"""
def get_top_20_popular_movies(movies):
    # Get the top 20 popular movies in order to resolve cold starting issues primarily.
    sorted_movies = movies.sort_values(by=[ "vote_average", "vote_count"], ascending=[False, False])
    top_20_popular_movies = list(sorted_movies["movie_id"])[:20]
    return top_20_popular_movies

def map_movies(movies, ratings):
    # Construct a mapping between movie_id and index.
    movies_list = list(movies["movie_id"])
    movie_id_dict = {i: movies_list[i] for i in range(movies.shape[0])}
    movie_id_dict_reversed = {movies_list[i]: i for i in range(movies.shape[0])}
    dict_size = len(movie_id_dict_reversed)
    original_rating_movies = list(ratings["movie_id"])
    for movie in original_rating_movies:
        if movie not in movie_id_dict_reversed:
            movie_id_dict_reversed[movie] = dict_size
            movie_id_dict[dict_size] = movie
            dict_size += 1
    return movie_id_dict, movie_id_dict_reversed

def get_rating_users(ratings):
    # Return a set of users who has rated movies.
    rating_users = list(ratings["user_id"])
    rating_users = set(rating_users)
    return rating_users

def get_rating_movies(ratings):
    # Return a list of movies who has been rated.
    rating_movies = [movie_id_dict_reversed[i] for i in list(ratings["movie_id"])]
    rating_movies = list(set(rating_movies))
    return rating_movies
"""

def get_recommendation(algo, userid):
    if userid not in rating_users:
        return top_20_popular_movies[:10]
    prediction = [(i, algo.predict(userid, i).est) for i in rating_movies]
    prediction.sort(key = lambda x: x[1], reverse = True)
    #print("The first 20 prediction is ",prediction[:20])
    result = [movie_id_dict[item[0]] for item in prediction[:10]]
    return result

def load_model(model_filename):
    print (">> Loading dump")
    from surprise import dump
    import os
    file_name = os.path.expanduser(model_filename)
    _, loaded_model = dump.load(file_name)
    print (">> Loaded dump")
    return loaded_model

def train(algo, trainset, testset):
    start_time = time.time()
    algo.fit(trainset)
    print("The model training time is ", time.time() - start_time)
    start_time = time.time()
    predictions = algo.test(testset)
    print("The RMSE is ", rmse(predictions))
    print("The MSE is ", mse(predictions))
    print("The MAE is ", mae(predictions))
    print("The model prediction time is ", time.time() - start_time)


if __name__ == '__main__':
    
    """
    movies_df, users_df, ratings_df = get_data()
    top_20_popular_movies = get_top_20_popular_movies(movies_df)
    movie_id_dict, movie_id_dict_reversed = map_movies(movies_df, ratings_df)
    rating_users = get_rating_users(ratings_df)
    rating_movies = get_rating_movies(ratings_df)
    #ratings_df['movie_id'].replace(movie_id_dict_reversed, inplace=True) 
    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(ratings_df[["user_id", "movie_id", "rating"]], reader)
    trainset, testset = train_test_split(data, test_size=.2, train_size=None, random_state=100, shuffle=True)
    """
    min_users_rating = 5 #int(sys.argv[1]) 
    min_movies_rating = 10 #int(sys.argv[2]

    movies, users, original_ratings = get_data()
    ratings = clean(original_ratings)
    movie_id_dict, movie_id_dict_reversed = map_movies(movies, ratings)
    user_id_dict, user_id_dict_reversed = map_users(users, ratings)
    rating_users = get_rating_users(ratings, min_users_rating)
    rating_movies = get_rating_movies(ratings, min_movies_rating)
    top_50_popular_movies = get_top_50_popular_movies(movies)

    df_new = ratings[(ratings['movie_id'].isin(rating_movies)) & (ratings['user_id'].isin(rating_users))]
    df_new["user_id"] = df_new["user_id"].map(user_id_dict_reversed)
    df_new["movie_id"] = df_new["movie_id"].map(movie_id_dict_reversed)
    print('The original data frame shape:\t{}'.format(ratings.shape))
    print('The new data frame shape:\t{}'.format(df_new.shape))
    print("> OK")

    reader = Reader(rating_scale=(1, 5))
    if df_new.shape[0] > 30000:
        print("Too many data, needs to clip to 30,000!")
        df_new = df_new[:30000]
    #trainset, testset = train_test_split(df_new, test_size=.25, random_state=11695, shuffle=True)
    rating_data = Dataset.load_from_df(df_new[["user_id", "movie_id", "rating"]], reader)
    trainset, testset = train_test_split(rating_data, test_size=.2, random_state=100, shuffle=True)

    """
    lr_all is the learning rate for all parameters (how much the parameters are adjusted in each iteration)
    reg_all is the regularization term for all parameters, which is a penalty term added to prevent overfitting.
    """

    param_grid = {
        "n_epochs": [5, 10],
        "lr_all": [0.002, 0.004],
        "reg_all": [0.4, 0.6]
    }
    
    # Get the best params using GridSearchCV
    
    gs = GridSearchCV(SVD, param_grid, measures=["rmse"], cv=3)
    gs.fit(rating_data)
    best_params = gs.best_params["rmse"]
    
    
    # Extract and train model with best params
    

    start_time = time.time()
    print("Training Model")
    svd_algo = SVD(n_epochs=best_params['n_epochs'],
    lr_all=best_params['lr_all'],
    reg_all=best_params['reg_all'])
    
    train(svd_algo, trainset, testset)
    
    svd_algo.fit(trainset)

    print("model size (in bytes): {}".format(sys.getsizeof(svd_algo.pu) + sys.getsizeof(svd_algo.qi) + sys.getsizeof(svd_algo.bu) + sys.getsizeof(svd_algo.bi)))

    model_filename = "./cf_svd_model.pickle"
    dump.dump(model_filename, algo=svd_algo)

    """
    result_dict = {}
    for userid in rating_users:
        result = get_recommendation(svd_algo, userid)
        result_dict[userid] = result
    with open("cf_svd_rating_result_full.json", "w") as outfile:
        json.dump(result_dict, outfile)
    """