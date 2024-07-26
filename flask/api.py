import sys

sys.path.append("/home/lfgomes/group-project-s22-dsu/")

from flask import Flask, make_response
from data_quality.api_request_check import *


from recom_manager import RecommenderManager

app = Flask(__name__)
rmanager = RecommenderManager()


@app.route("/recommend/<userid>", methods=["GET"])
def recommend(userid):
    if valid_user_id_check(userid):
        recommend_movies = rmanager.get_recommendations(userid)
        recommend_movies = ",".join(recommend_movies)
        response = make_response(recommend_movies, 200)
        response.mimetype = "text/plain"
    else:
        response = make_response("Error", 200)
    return response


if __name__ == "__main__":
    # app.run(host="128.2.205.106", port=8082, debug=True)
    app.run(host="128.2.205.106", port=8082, debug=True)
