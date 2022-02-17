from re import findall

def validate_keys(data: dict):
    valid_keys = ["name", "email", "phone"]
    invalid_keys = []
    
    for key in data.keys():
        if key not in valid_keys:
            invalid_keys.append(key)

    return valid_keys, invalid_keys

def is_valid_phone(phone: str):
    valid_format = "([(][0-9]{2}[)])([0-9]{5})([-])([0-9]{4})"

    if findall(valid_format, phone):
        return True
    
    return False

def is_valid_data_type(data: dict):
    for value in data.values():    
        if type(value) != str:
            return False
    return True

def is_valid_email_key(data: dict):
    for key in data.keys():
        if key != "email":
            return False
    return True