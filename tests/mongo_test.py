import sys

sys.path.append("/home/lfgomes/group-project-s22-dsu/")
sys.path.append("../mongodb")
from mongodb.db import client, get_movie, get_user

mongo = client
production_db = client["production"]


def test_insert_user():
    # Create a user
    user = {
        "user_id": 10000,
        "age": 26,
        "gender": "M",
        "occupation": "self-employed",
    }
    user_id = user["user_id"]
    col = production_db["users"]
    x = col.update_one(
        {"user_id": user_id},
        {"$set": user},
        upsert=True,
    )
    inserted_user = get_user(user_id)
    for key in user:
        assert inserted_user[key] == user[key]


def test_insert_movie():
    # Create a movie
    movie = {
        "movie_id": "the+pirate+bay+away+from+keyboard+2013",
        "adult": "False",
        "belongs_to_collection": {},
        "budget": "0",
        "genres": [{"id": 99, "name": "Documentary"}],
        "homepage": "http://www.tpbafk.tv/",
        "id": "the+pirate+bay+away+from+keyboard+2013",
        "imdb_id": "tt2608732",
        "original_language": "en",
        "original_title": "The Pirate Bay: Away From Keyboard",
        "overview": "TPB AFK is a documentary about three computer addicts who redefined the world of media distribution with their hobby homepage The Pirate Bay. How did Tiamo, a beer crazy hardware fanatic, Brokep a tree hugging eco activist and Anakata – a paranoid hacker libertarian – get the White House to threaten the Swedish government with trade sanctions? TPB AFK explores what Hollywood’s most hated pirates go through on a personal level.",
        "popularity": "4.02059",
        "poster_path": "/9RsWRiwtnc07SbOfqN47XLqKcdo.jpg",
        "production_companies": [
            {"name": "Danmarks Radio (DR)", "id": 119},
            {"name": "SVT", "id": 3179},
            {"name": "Norsk Rikskringkasting (NRK)", "id": 5404},
            {"name": "BBC", "id": 5996},
            {"name": "ZDF Productions", "id": 8595},
            {"name": "Piraya Film A/S", "id": 29063},
        ],
        "production_countries": [{"iso_3166_1": "SE", "name": "Sweden"}],
        "release_date": "2013-02-08",
        "revenue": "34664",
        "runtime": 82,
        "spoken_languages": [
            {"iso_639_1": "en", "name": "English"},
            {"iso_639_1": "sv", "name": "svenska"},
        ],
        "status": "Released",
        "title": "The Pirate Bay: Away From Keyboard",
        "tmdb_id": 50275,
        "vote_average": "7.0",
        "vote_count": "123",
    }

    movie_id = movie["movie_id"]
    col = production_db["movies"]
    x = col.update_one(
        {"movie_id": movie_id},
        {"$set": movie},
        upsert=True,
    )

    inserted_movie = get_movie(movie_id)
    for key in movie:
        assert inserted_movie[key] == movie[key]
