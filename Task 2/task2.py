from types import List, dict
from re import sub

def cleanId(id):
    return sub(r'[^0-9]', '', id)



def merge_list():
    pass

if __name__ == "__main__":
    Users = [{ "user_ref": "ID_101", "name": "Alice" }, { "user_ref": "#102", "name": "Bob" }]
    Scores = [{ "id": "101", "score": 88 }, { "id": "102", "score": 95 }]
