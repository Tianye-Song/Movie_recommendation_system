from random import random
import sys
import random

sys.path.append("/home/lfgomes/group-project-s22-dsu")
import db_manager as db


def get_recommendations(user_id):
    user = db.get_user(user_id)
    if user:
        # TODO Get recommendations for this user
        print(user["occupation"])
    else:
        # TODO Get random recommendations.
        # The user is new, we don't have information yet
        print("user not found", user_id)
    # ... user_rates = db.get_rates(user_id...)
    # TODO Complete to get data and query ML model
    some_movies = [movie["id"] for movie in db.get_movies(50)]
    recommendations = random.sample(some_movies, 20)

    return recommendations
