from urllib import response
import re

example = "2022-02-08T12:02:38.164729,141977,recommendation request 17645-team04.isri.cmu.edu:8082, status 200, result: mona+lisa+1986, interstellar+2014, the+lord+of+the+rings+the+fellowship+of+the+ring+2001, the+public+enemy+1931, vampire+hunter+d+bloodlust+2000, les+misrables+1998, mickey_+donald_+goofy+the+three+musketeers+2004, walle+2008, samsara+2001, seven+samurai+1954, from+russia+with+love+1963, for+those+in+peril+2013, shaolin+soccer+2001, the+matrix+1999, the+good_+the+bad+and+the+ugly+1966, my+neighbor+totoro+1988, out+cold+2001, bonnie+and+clyde+1967, murder+at+1600+1997, our+paradise+2011, 89 ms"


class Parser:
    def __init__(self):
        self.watch_column_names = ("time_read", "user_id", "movie_id", "time")
        self.rating_column_names = ("time_read", "user_id", "movie_id", "rating")
        self.recommendation_column_names = (
            "time_read",
            "user_id",
            "server_address",
            "recommendations",
            "response_time",
            "status",
        )

    def parse(self, text):
        # need to identify the 3 types of messages and then parse each seperately.

        parts = text.split(",")

        if len(parts) == 3:
            # case that message is either watch data or rating
            if parts[2][5:9] == "data":
                return self.parse_watch(parts)
            elif parts[2][5:9] == "rate":
                return self.parse_rating(parts)
            else:
                raise ValueError("Wrong value.")
        else:
            # case that message is a request
            return self.parse_recommendation_request(text)

    def parse_watch(self, parts):
        time_read, user_id, data = parts
        get_request = data.split()[1].split("/")
        movie, time = get_request[3], int(get_request[4].replace(".mpg", ""))
        return dict(zip(self.watch_column_names, (time_read, user_id, movie, time)))

    def parse_rating(self, parts):
        time, user_id, data = parts
        movie, rating = data[10:].split("=")
        rating = int(rating)
        return dict(zip(self.rating_column_names, (time, user_id, movie, rating)))

    def parse_recommendation_request(self, text):
        # print(text)
        parts = text.split(",")
        time_read, user_id, request_text, status = (
            parts[0],
            parts[1],
            parts[2],
            parts[3],
        )
        server = request_text.split()[-1]
        status = int(status.split()[1])
        recommendations_and_response_time = re.findall("(?<=result: ).*", text)[
            0
        ].split(", ")

        recommendations, response_time = (
            recommendations_and_response_time[
                0 : len(recommendations_and_response_time) - 1
            ],
            recommendations_and_response_time[-1],
        )
        response_time = int(response_time.split(" ")[0])
        """
        if status != 200:
            raise Exception("status is wrong")
        """

        return dict(
            zip(
                self.recommendation_column_names,
                (time_read, user_id, server, recommendations, response_time, status),
            )
        )
