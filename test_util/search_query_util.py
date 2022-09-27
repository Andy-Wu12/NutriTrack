import string


def create_search_form(query: str):
    return {'query': query}


def get_invalid_query_input(food_name: str, username: str):
    # Since queries are case-insensitive, only use either lowercase or uppercase
    base_ascii = set(string.ascii_lowercase) | set(string.digits)
    valid_query_inputs = set(food_name.lower()) | set(username.lower())
    return base_ascii - valid_query_inputs
