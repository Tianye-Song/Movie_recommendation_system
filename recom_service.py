from flask import Flask, make_response


from recom_manager import RecommenderManager2

app = Flask(__name__)

rmanager_m1 = RecommenderManager2("m1")
rmanager_m2 = RecommenderManager2("m2")


@app.route("/get_recommendations/<userid>", methods=["GET"])
def get_recommendations(userid):
    if int(userid) < 5000:
        print("Using model M1!")
        recommend_movies = rmanager_m1.get_recommendations(userid)
        recommend_movies = ",".join(recommend_movies)
        response = make_response(recommend_movies, 200)
        response.mimetype = "text/plain"

    else:
        print("Using model M2!")
        recommend_movies = rmanager_m2.get_recommendations(userid)
        recommend_movies = ",".join(recommend_movies)
        response = make_response(recommend_movies, 200)
        response.mimetype = "text/plain"

    return recommend_movies


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True)
