import numpy as np
import pandas as pd
from datetime import datetime
import re

#For all the collections inluding view_history, rates, movies and rates
def insert_missing_keys(input_dict_data, col_name):
    """insert missing fields for the streaming data

    Args:
        input_dict_data (dict): input dictionary data 
        col_name (str): name of the collection

    Returns:
        dict: dictionary after change
    """
    # Define the field set that should have
    if col_name == "views_history":
        col_set = ["time_read","movie_id","time","user_id"]
    elif col_name == "rates":
        col_set = ["time_read","rating","user_id","movie_id"]
    elif col_name == "movies":
        col_set = ['movie_id', 'adult', 'belongs_to_collection',
                   'budget', 'genres', 'homepage', 'id', 'imdb_id',
                   'original_language', 'original_title', 'overview',
                   'popularity', 'poster_path', 'production_companies', 
                   'production_countries', 'release_date', 'revenue',
                   'runtime', 'spoken_languages', 'status', 'title', 
                   'tmdb_id', 'vote_average', 'vote_count']
    elif col_name == "users":
        col_set = ["user_id","age","gender","occupation"]
    else:
        print("invalid collection name")
        return input_dict_data
    
    for key_name in col_set:
        if key_name not in input_dict_data.keys():
            input_dict_data[key_name] = np.nan
            
    return input_dict_data

# For all the collections that contain string data
def trim_str_value(input_dict_data):
    """Delete unnecessary white space of string data

    Args:
        input_dict_data (dict): 
    
    Returns:
        dict: updated dict
    """
    for key_name in input_dict_data.keys():
        value = input_dict_data[key_name]
        if isinstance(value, str):
            input_dict_data[key_name] = value.strip()
    return input_dict_data

# For all the collections that contain string data
def update_missing_values(input_dict_data):
    """Update empty string to be np.nan

    Args:
        input_dict_data (dict): input dict

    Returns:
        dict: updated dict
    """
    for key_name in input_dict_data.keys():
        value = input_dict_data[key_name]
        if isinstance(value, str):
            if value == "":
                input_dict_data[key_name] = np.nan 
    return input_dict_data 

#For collection rates and views_history which contain "time_read" field         
def transfer_date_data(input_dict_data):
    """transfer string date data to be datetime data

    Args:
        input_dict_data (dict): input dictionary data

    Returns:
        dict: updated dictionary data
    """
    value = input_dict_data["time_read"]
    if not pd.isnull(value):
        try:
            time_data = datetime.strptime(value,"%Y-%m-%dT%H:%M:%S")
        except:
            if(value[5:7]>"12")&(value[8:10]<"12"):
                value = value[:5]+value[8:10]+value[4:7]+value[10:]
                try:
                    time_data = datetime.strptime(value,"%Y-%m-%dT%H:%M:%S")
                except:
                    time_data = np.nan  
            else:
                time_data = np.nan    
        finally:
            input_dict_data["time_read"] = time_data
    return input_dict_data
        
# For collection rates, views_history and users which contain "user_id" field
def check_user_id(input_dict_data):
    """check "user_id" to make sure it is int type

    Args:
        input_dict_data (dict): input dictionary data
        
    Returns:
        dict: updated dictionary data
    """
    user_id = input_dict_data["user_id"]
    if not pd.isnull(user_id):
        if isinstance(user_id, str):
            if(bool(re.match('^[0-9]+$', user_id))):
                user_id = int(user_id)
            else:
                user_id = np.nan
        elif(isinstance(user_id, int)):
            pass
        else:
            user_id = np.nan
    input_dict_data["user_id"] = user_id
    return input_dict_data
 
# For collection rates that contain "rating" field    
def check_rates_data(input_dict_data):
    """keep the range of rating between 1~5 and data type be int

    Args:
        input_dict_data (dict): input dictionary data

    Returns:
        dict: updated dictionary data
    """
    rates = input_dict_data["rating"]
    if not pd.isnull(rates):
        if isinstance(rates,str):
            try:
                rates = int(rates)
                if(rates>5)|(rates<1):
                    rates = np.nan
            except:
                rates = np.nan
        elif isinstance(rates, int):
            if(rates>5)|(rates<1):
                rates = np.nan
        else:
            rates = np.nan
    input_dict_data["rating"] = rates
    return input_dict_data

# For collection users that contain "age" field        
def check_age_data(input_dict_data):
    """check age data to make sure the range of age is between 0~100

    Args:
        input_dict_data (dict): input dictionary data

    Returns:
        dict: updated dictionary data
    """
    age = input_dict_data['age']
    if not pd.isnull(age):
        if isinstance(age,str):
            try:
                age = int(age)
                if (age<0)|(age>100):
                    age = np.nan
            except:
                age = np.nan
        elif isinstance(age, int):
            if (age<0)|(age>100):
                age = np.nan
        else:
            age = np.nan
    input_dict_data["age"] = age
    return input_dict_data

#Integrated functions for different collections

def check_views_history(input_dict_data):
    input_dict_data = insert_missing_keys(input_dict_data, "views_history")
    input_dict_data = trim_str_value(input_dict_data) 
    input_dict_data = update_missing_values(input_dict_data)
    input_dict_data = transfer_date_data(input_dict_data)
    input_dict_data = check_user_id(input_dict_data)
    return input_dict_data

def check_rates(input_dict_data):
    input_dict_data = insert_missing_keys(input_dict_data, "rates")
    input_dict_data = trim_str_value(input_dict_data) 
    input_dict_data = update_missing_values(input_dict_data)
    input_dict_data = transfer_date_data(input_dict_data)
    input_dict_data = check_rates_data(input_dict_data)
    input_dict_data = check_user_id(input_dict_data)
    return input_dict_data


def check_movies(input_dict_data):
    input_dict_data = insert_missing_keys(input_dict_data, "movies")
    input_dict_data = trim_str_value(input_dict_data) 
    input_dict_data = update_missing_values(input_dict_data)
    return input_dict_data
        

def check_users(input_dict_data):
    input_dict_data = insert_missing_keys(input_dict_data, "users")
    input_dict_data = trim_str_value(input_dict_data) 
    input_dict_data = update_missing_values(input_dict_data)
    input_dict_data = check_age_data(input_dict_data)
    input_dict_data = check_user_id(input_dict_data)
    return input_dict_data
    
        
          