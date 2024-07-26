import random
import db_manager as dbm


class RecommenderManager:
    def __init__(self):
        self.recommendations = dbm.get_recommendations()

    def get_recommendations(self, user_id):
        user_id = str(user_id)
        shuffle = False
        if user_id not in self.recommendations:
            user_id = "NA"
            shuffle = True

        movies = self.recommendations[user_id]
        if shuffle:
            random.shuffle(movies)

        return movies[:20]


class RecommenderManager2:
    def __init__(self, model_name):
        self.recommendations = dbm.get_recommendations(model_name)

    def get_recommendations(self, user_id):
        user_id = str(user_id)
        shuffle = False
        if user_id not in self.recommendations:
            user_id = "NA"
            shuffle = True

        movies = self.recommendations[user_id]
        if shuffle:
            random.shuffle(movies)

        return movies[:20]
