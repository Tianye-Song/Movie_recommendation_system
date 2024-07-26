from data import get_data

# Clean the ratings.csv, drop out those ratings with nan values.
def clean(ratings):
    print(">Start cleaning")
    print("The initial ratings has records ", ratings.shape[0])
    ratings = ratings.dropna()
    print("The clean ratings has records ", ratings.shape[0])
    return ratings

# Collect the true watching and rating hostory for users, which is used for online evaluation.
def collect_rating_records(ratings):
    records = {}
    for index,row in ratings.iterrows():
        user = str(row['user_id'])
        movie = row['movie_id']
        score = row['rating']
        time = row['time_read']
        if user not in records:
            records[user] = {}
        records[user][movie] = score
    return records

# Construct the dict and revere dict to map movie id to integer id.
'''
def map_movies(movies, ratings, verbose=True):
    # Construct a mapping between movie_id and index.
    movies_list = list(movies["movie_id"])
    movie_id_dict = {i: movies_list[i] for i in range(movies.shape[0])}
    movie_id_dict_reversed = {movies_list[i]: i for i in range(movies.shape[0])}
    dict_size = len(movie_id_dict_reversed)
    if verbose:
        print("The original movie dict size is ", dict_size)
    original_rating_movies = list(ratings["movie_id"])
    for movie in original_rating_movies:
        if movie not in movie_id_dict_reversed:
            movie_id_dict_reversed[movie] = dict_size
            movie_id_dict[dict_size] = movie
            dict_size += 1
    if verbose:
        print("The final movie dict size is ", dict_size)
    return movie_id_dict, movie_id_dict_reversed
'''
def map_movies(ratings, verbose=True):
    # Construct a mapping between movie_id and index.
    movies_list = list(ratings["movie_id"].unique())
    movie_id_dict = {i: movies_list[i] for i in range(len(movies_list))}
    movie_id_dict_reversed = {movies_list[i]: i for i in range(len(movies_list))}
    dict_size = len(movie_id_dict_reversed)
    if verbose:
        print("The final movie dict size is ", dict_size)
    return movie_id_dict, movie_id_dict_reversed

# Construct the dict and revere dict to map user id to integer id.
'''
def map_users(users, ratings, verbose=True):
    # Construct a mapping between user_id and index.
    users_list = list(users["user_id"])
    user_id_dict = {i: users_list[i] for i in range(users.shape[0])}
    user_id_dict_reversed = {users_list[i]: i for i in range(users.shape[0])}
    dict_size = len(user_id_dict_reversed)
    if verbose:
        print("The original user dict size is ", dict_size)
    original_rating_users = list(ratings["user_id"])
    for user in original_rating_users:
        if user not in user_id_dict_reversed:
            user_id_dict_reversed[user] = dict_size
            user_id_dict[dict_size] = user
            dict_size += 1
    if verbose:
        print("The final user dict size is ", dict_size)
    return user_id_dict, user_id_dict_reversed
'''
def map_users(ratings, verbose=True):
    # Construct a mapping between user_id and index.
    users_list = list(ratings["user_id"].unique())
    user_id_dict = {i: int(users_list[i]) for i in range(len(users_list))}
    user_id_dict_reversed = {int(users_list[i]): i for i in range(len(users_list))}
    dict_size = len(user_id_dict_reversed)
    if verbose:
        print("The final user dict size is ", dict_size)
    return user_id_dict, user_id_dict_reversed



def get_rating_users(ratings, min_users_rating, verbose=True):
    # Return a set of users who has rated movies.
    filter_users = ratings['user_id'].value_counts() > min_users_rating
    filter_users = filter_users[filter_users].index.tolist()
    if verbose:
        print("The number of users rating is ", len(filter_users))
    return filter_users

def get_rating_movies(ratings, min_movies_rating, verbose=True):
    # Return a list of movies who has been rated.
    filter_movies = ratings['movie_id'].value_counts() > min_movies_rating
    filter_movies = filter_movies[filter_movies].index.tolist()
    if verbose:
        print("The number of movies rated is ", len(filter_movies))
    return filter_movies

def get_top_50_popular_movies(movies):
    # Get the top 20 popular movies in order to resolve cold starting issues primarily.
    frequent_movies = movies.sort_values(by="vote_count", ascending=False)
    frequent_movies = frequent_movies[:100]
    #print("The frequent_movies is ",  frequent_movies[:50][["vote_average", "vote_count"]])
    sorted_movies = frequent_movies.sort_values(by="vote_average", ascending=False)
    #print("The sorted_movies is ",  sorted_movies[:10][["vote_average", "vote_count"]])
    top_50_popular_movies = list(sorted_movies["movie_id"])[:50]
    return top_50_popular_movies

if __name__ == '__main__':
    movies, users, original_ratings = get_data()
    ratings = clean(original_ratings)
    print(ratings.columns)
    collect_rating_records(ratings)