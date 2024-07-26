import re

def valid_user_id_check(user_id):
    """check whether the request user_id is in a correct format

    Args:
        user_id (_type_): _description_

    Returns:
        _type_: bool value
        
    """
    if user_id:
        if(bool(re.match('^[0-9]+$', user_id))):
            return True
        else:
            return False
    else: 
        return False