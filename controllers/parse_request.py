from flask import request


def get_request_data():
    """
    Get keys & values from request (Note that this method should parse requests with content type "application/x-www-form-urlencoded")
    """
    data = {}
    for key, value in request.form.items():
        data[key] = value

    return data