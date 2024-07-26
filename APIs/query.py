import requests

IP = "128.2.204.215:8080"
VIRTUAL = "128.2.205.106:8082"

# Get the user JSON file from userid and IP address.
def getuser(ip, userid):
    url = "http://" + str(ip) + "/user/" + str(userid)
    response = requests.get(url)
    status = response.status_code
    if status != 200:
        return None
    user_info = response.json()
    return user_info


# Get the movie JSON file from movieid and IP address.
def getmovie(ip, movieid):
    url = "http://" + str(ip) + "/movie/" + str(movieid)
    response = requests.get(url)
    status = response.status_code
    if status != 200:
        return None
    movie_info = response.json()
    return movie_info


# Retrieve the recommendation result from the system by userid.
def retrieve(virtual_address, userid):
    url = "http://" + str(virtual_address) + "/recommend/" + str(userid)
    response = requests.get(url)
    status = response.status_code
    if status != 200:
        return None
    result = response.json()
    return result


# userid = 430057
# print(getuser(IP, userid))

# movieid = "chain+reaction+1996"
# print(getmovie(IP, movieid))
