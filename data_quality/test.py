from db_quality_check import *


users = {
        "user_id" : "1234",
        "age" : 3.5,
        "gender" : "M",
        "occupation" : "self-employed"
}

views_history = {
        "time_read" : "2022-02-04T20:35:53",
        "movie_id" : "dallas+buyers+club+2013 ",
         "time" : 70,
        "user_id" : ""
}

rates = {
        "movie_id" : "geronimo+an+american+legend+1993",
        "user_id" : "225022",
        "rating" : np.nan,
        "time_read" : "2022-13-06T17:00:17"
}

movies = {
        "movie_id" : "the+pirate+bay+away+from+keyboard+2013",
        "adult" : "False",
        "belongs_to_collection" : {

        },
        "budget" : "0",
        "genres" : [
                {
                        "id" : 99,
                        "name" : "Documentary"
                }
        ],
        "homepage" : "http://www.tpbafk.tv/",
        "id" : "the+pirate+bay+away+from+keyboard+2013",
        "imdb_id" : "tt2608732",
        "original_language" : "en",
        "original_title" : "The Pirate Bay: Away From Keyboard",
        "overview" : "TPB AFK is a documentary about three computer addicts who redefined the world of media distribution with their hobby homepage The Pirate Bay. How did Tiamo, a beer crazy hardware fanatic, Brokep a tree hugging eco activist and Anakata – a paranoid hacker libertarian – get the White House to threaten the Swedish government with trade sanctions? TPB AFK explores what Hollywood’s most hated pirates go through on a personal level.",
        "popularity" : "4.02059",
        "poster_path" : "/9RsWRiwtnc07SbOfqN47XLqKcdo.jpg",
        "production_companies" : [
                {
                        "name" : "Danmarks Radio (DR)",
                        "id" : 119
                },
                {
                        "name" : "SVT",
                        "id" : 3179
                },
                {
                        "name" : "Norsk Rikskringkasting (NRK)",
                        "id" : 5404
                },
                {
                        "name" : "BBC",
                        "id" : 5996
                },
                {
                        "name" : "ZDF Productions",
                        "id" : 8595
                },
                {
                        "name" : "Piraya Film A/S",
                        "id" : 29063
                }
        ],
        "production_countries" : [
                {
                        "iso_3166_1" : "SE",
                        "name" : "Sweden"
                }
        ],
        "release_date" : "2013-02-08",
        "revenue" : "34664",
        "runtime" : 82,
        "spoken_languages" : [
                {
                        "iso_639_1" : "en",
                        "name" : "English"
                },
                {
                        "iso_639_1" : "sv",
                        "name" : "svenska"
                }
        ],
        "status" : "Released",
        "title" : "The Pirate Bay: Away From Keyboard",
        "tmdb_id" : 50275,
        "vote_average" : "7.0",
        "vote_count" : "123"
}

isinstance([1,2,3], list)

# value = "2022-13-06T17:00:17"
# print(value[5:7]>"12")
# print(value[8:10]<"12")