import math
import sys
import random

sys.path.append("/home/lfgomes/group-project-s22-dsu/flask")

# from group-project-s22-dsu.flask.api import recommend,get_user_id
from api import app

client = app.test_client()


def test_recommend():
    # Test 1 : Check for the same integer values
    ids = [0, 00, 000, 0000]
    response_list = []
    for id_ in ids:
        path = f"/recommend/{id_}"
        response = client.get(path)
        response_list.append(response.data)
        assert response.status_code == 200
        assert type(response.data).__name__ == "bytes"
        assert len(str(response.data).split(",")) == 20

    # Test 2 : Check for some random integer value
    # sys.maxint : represents the maximum value of an integer
    # -sys.maxint - 1 : represents the minimum value of an integer
    rand_int = random.randint(0, 1000000)
    path = f"/recommend/{rand_int}"
    response = client.get(path)
    assert response.status_code == 200
    assert type(response.data).__name__ == "bytes"
    assert len(str(response.data).split(",")) == 20

    # Test 3 : Check for a value outside the bounds.
    float_value = float("inf")
    path = f"/recommend/{float_value}"
    response = client.get(path)
    assert response.data.decode("UTF-8") == "Error"

    # Check for non-integer values
    # Test 4 : Testing with a string name : tushar
    path = f"/recommend/tushar"
    response = client.get(path)
    assert response.data.decode("UTF-8") == "Error"

    # Test 5 : Testing with log values which are not integers
    val = math.log(10)
    path = f"/recommend/{val}"
    response = client.get(path)
    assert response.data.decode("UTF-8") == "Error"
