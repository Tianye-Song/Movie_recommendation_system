import sys
import os
from datetime import date, timedelta

sys.path.append("/home/lfgomes/group-project-s22-dsu/")
from db_manager import get_movies_df, get_users_df, get_rates_df, get_rates_df_latest


def get_data(verbose=True):
    movies = get_movies_df()
    if verbose:
        print("The number of movies we get is", movies.shape[0])
    users = get_users_df()
    if verbose:
        print("The number of users we get is", users.shape[0])
    ratings = get_rates_df()
    if verbose:
        print("The number of ratings we get is", ratings.shape[0])
    return movies, users, ratings


def get_latest_data(startday, endday, verbose=True):
    movies = get_movies_df()
    if verbose:
        print("The number of movies we get is", movies.shape[0])
    my_date = date.today()
    datelist = [
        (my_date - timedelta(days=N)).strftime("%Y-%m-%d")
        for N in range(startday, endday)
    ]
    ratings = get_rates_df_latest(datelist)
    if verbose:
        print("The number of ratings we get is", ratings.shape[0])
    return movies, ratings


if __name__ == "__main__":
    moviers, ratings = get_latest_data(1, 8)
