import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
client2 = pymongo.MongoClient("mongodb://mongoservice:27017/")

test_db = client["test"]
production_db = client["production"]
production_db2 = client2["production"]


def insert_user(user_id, user):
    col = production_db["users"]
    x = col.update_one(
        {"user_id": user_id},
        {"$set": user},
        upsert=True,
    )
    return x


def insert_recommendation(user_id, recommendation):
    col = production_db["recommendations"]
    x = col.update_one(
        {"user_id": user_id},
        {"$set": recommendation},
        upsert=True,
    )
    return x


def insert_recommendation_m1(user_id, recommendation):
    col = production_db["recommendations_m1"]
    x = col.update_one(
        {"user_id": user_id},
        {"$set": recommendation},
        upsert=True,
    )
    return x


def insert_recommendation_m2(user_id, recommendation):
    col = production_db["recommendations_m2"]
    x = col.update_one(
        {"user_id": user_id},
        {"$set": recommendation},
        upsert=True,
    )
    return x


def insert_rate(rate):
    col = production_db["rates"]
    x = col.update_one(
        {"user_id": rate["user_id"], "movie_id": rate["movie_id"]},
        {"$set": rate},
        upsert=True,
    )
    return x


def insert_movie(movie_id, movie):
    col = production_db["movies"]
    x = col.update_one(
        {"movie_id": movie_id},
        {"$set": movie},
        upsert=True,
    )
    return x


def insert_view_history(view):
    col = production_db["views_history"]
    x = col.insert_one(view)
    return x


def insert_recommend_history(view):
    col = production_db["recommend_history"]
    x = col.insert_one(view)
    return x


def get_user(user_id):
    col = production_db["users"]
    user = col.find_one({"user_id": user_id})
    return user


def get_movie(movie_id):
    col = production_db["movies"]
    movie = col.find_one({"movie_id": movie_id})
    return movie


def get_movies(n=0, query={}, projection={}):
    col = production_db["movies"]
    movies = col.find(query, projection).limit(n)
    return movies


def get_users(n=0, query={}, projection={}):
    col = production_db["users"]
    users = col.find(query, projection).limit(n)
    return users


def get_rates(n=0, query={}, projection={}):
    col = production_db["rates"]
    users = col.find(query, projection).limit(n)
    return users


def get_rates_latest(date):
    col = production_db["rates"]
    x = col.find({"time_read": {"$regex": date}})
    return x


def get_recommendations(n=0, query={}, projection={}):
    col = production_db["recommendations"]
    recommendations = col.find(query, projection).limit(n)
    return recommendations


def get_recommendations2(model_name, n=0, query={}, projection={}):
    col_name = "recommendations_" + model_name
    col = production_db2[col_name]
    recommendations = col.find(query, projection).limit(n)
    return recommendations


def get_recommendation_history(date):
    col = production_db["recommend_history"]
    x = col.find({"time_read": {"$regex": date}})
    return x


# get recommendation history between two dates
def get_recommendation_history_between(date1, date2):
    col = production_db["recommend_history"]
    x = col.find({"time_read": {"$gt": date1, "$lt": date2}})
    return x
