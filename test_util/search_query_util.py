import string
from typing import List

def create_search_form(query: str):
    return {'query': query}


def get_invalid_query_input(query_inputs: List[str]):
    # Since queries are case-insensitive, only use either lowercase or uppercase
    base_ascii = set(string.ascii_lowercase) | set(string.digits)
    query_char_set = set()

    for query in query_inputs:
        query_char_set = query_char_set | set(query.lower())

    return base_ascii - query_char_set
