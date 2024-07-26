import sys

IP = "128.2.204.215:8080"
VIRTUAL = "128.2.205.106:8082"
sys.path.append("/home/lfgomes/group-project-s22-dsu/mongodb")
sys.path.append("/home/lfgomes/group-project-s22-dsu/APIs")
from db import *
from query import getuser, getmovie


def test_getuser():
    # check for random users
    user_ids = [0, 120, 9999, 10111101]
    for user_id in user_ids:
        if get_user(user_id) is not None:
            assert type(getuser(IP, user_id)) is dict
        else:
            assert (getuser(IP, user_id)) is None


def test_getmovie():
    # check for random movie ids
    movie_ids = [
        "the+pirate+bay+away+from+keyboard+2013",
        "the+lawless+1950",
        "stella+street+2004",
        "tushar+vatsa+2005",
        "luis+fernandes+gomes+2010",
    ]
    for movie_id in movie_ids:
        if get_movie(movie_id) is not None:
            assert type(getmovie(IP, movie_id)) is dict
        else:
            assert (getmovie(IP, movie_id)) is None
