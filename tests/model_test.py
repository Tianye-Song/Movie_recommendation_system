from surprise import Reader
from surprise import KNNWithMeans
from surprise.model_selection import train_test_split
from surprise import Dataset
from surprise.accuracy import rmse, mse, mae
import sys

sys.path.append("..")
from db_manager import get_movies_df, get_users_df, get_rates_df
import time

sys.path.append("/home/lfgomes/group-project-s22-dsu/")

sys.path.append("../ml")
from ml.KNN import *


def test_model():
    movies_df = get_movies_df().head(50)
    users_df = get_users_df().head(50)
    ratings_df = get_rates_df().head(50)
    top_50_popular_movies = get_top_50_popular_movies(movies_df)
    movie_id_dict, movie_id_dict_reversed = map_movies(movies_df, ratings_df)
    rating_users = get_rating_users(ratings_df, 100)
    rating_movies = get_rating_movies(ratings_df, 100)
    ratings_df["movie_id"].replace(movie_id_dict_reversed, inplace=True)
    reader = Reader(rating_scale=(1, 10))

    # Creating a small mini dataset for testing
    rating_data = Dataset.load_from_df(
        ratings_df[["user_id", "movie_id", "rating"]][:10], reader
    )

    # Creating a training and test set based on test_size = 0.1
    trainset1, testset1 = train_test_split(
        rating_data, test_size=0.1, train_size=None, random_state=100, shuffle=True
    )
    # Creating a training and test set based on test_size = 0.5
    trainset2, testset2 = train_test_split(
        rating_data, test_size=0.5, train_size=None, random_state=100, shuffle=True
    )

    sim_options = {
        "name": "cosine",
        "user_based": True,
    }
    algo = KNNWithMeans(sim_options=sim_options)
    start_time = time.time()
    predictions1 = train(algo, trainset1, testset1)
    end_time = time.time()
    prediction_time1 = end_time - start_time

    start_time = time.time()
    predictions2 = train(algo, trainset2, testset2)
    end_time = time.time()
    prediction_time2 = end_time - start_time

    """
	Since we trained on bigger training set in case 1,
	our assumption is that accuracy will be higher in case 1
	"""
    # Test Case 1 : Check if the root mean square error for case 1 is higher compared to case 2.
    assert rmse(predictions1) < rmse(predictions2)

    # Test Case 2 : Check if the mean square error for case 1 is higher compared to case 2.
    assert mse(predictions1) < mse(predictions2)

    # Test Case 3 : Check if the mean absolute error for case 1 is higher compared to case 2.
    assert mae(predictions1) < mae(predictions2)

    # Test Case 4 : Check if the time taken for case 1 is more than time taken for case 2.
    assert prediction_time1 > prediction_time2


def train(algo, trainset, testset):
    start_time = time.time()
    algo.fit(trainset)
    start_time = time.time()
    predictions = algo.test(testset)
    return predictions
