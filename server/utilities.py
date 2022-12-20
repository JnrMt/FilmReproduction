import numpy as np

def get_from_string_to_original(string_array):
    array = []
    for string in string_array:
        array.append(float(string))  
    return np.asarray(array)

def get_users_from_string(string_array):
    array = []
    for string in string_array:
        array.append(string)  
    return array

def get_string_from_array(suggestions):
    return "/".join(x for x in suggestions)