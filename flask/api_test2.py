import sys
import requests

sys.path.append("/home/lfgomes/group-project-s22-dsu/")

from flask import Flask, make_response
from data_quality.api_request_check import *


app = Flask(__name__)


@app.route("/recommend/<userid>", methods=["GET"])
def recommend(userid):
    if valid_user_id_check(userid):
        recommend_movies = requests.get(
            "http://0.0.0.0:4000/get_recommendations/" + str(userid)
        ).content
        response = make_response(recommend_movies, 200)
        response.mimetype = "text/plain"
    else:
        response = make_response("Error", 200)

    return response


if __name__ == "__main__":
    app.run(host="128.2.205.106", port=7777, debug=True)
