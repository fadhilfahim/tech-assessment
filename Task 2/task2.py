from typing import List, Dict, Optional
import re

def cleanId(id):
    return re.search(r'\d+', id).group(0) if re.search(r'\d+', id) else None

def cleanUsers(Users: List[Dict]) -> None:
    for user in Users:
        raw_id = user.get('user_ref', '')
        user['user_ref'] = cleanId(raw_id)

def merge_list(Users: List[Dict], Scores: List[Dict]) -> List[Dict]:

    # create a dictionary to avoid looping through list multiple times
    score_dict = {score['id']: score['score'] for score in Scores}

    # merge with clean user ids
    merged_list = []
    for user in Users:
        user_id = user.get('user_ref')
        if user_id and user_id in score_dict:
            merged_user = {
                'user_ref': user_id,
                'name': user.get('name'),
                'score': score_dict[user_id]
            }
            merged_list.append(merged_user)
    return merged_list

def optimized_merge_list(Users: List[Dict], Scores: List[Dict]) -> List[Dict]:
    
    score_lookup = {score['id']: score['score'] for score in Scores}
    merged_list = []
    for user in Users:
        raw_id = user.get('user_ref', '')
        clean_id = cleanId(raw_id)
        merged_list.append({
            'user_ref': clean_id,
            'name': user.get('name'),
            'score': score_lookup.get(clean_id, None)
        })
    return merged_list

if __name__ == "__main__":

    # test
    Users = [{ "user_ref": "ID_101", "name": "Alice" }, { "user_ref": "#102", "name": "Bob" }]
    Scores = [{ "id": "101", "score": 88 }, { "id": "102", "score": 95 }]
    # clean data
    cleanUsers(Users)
    # print("Cleaned Users:", Users)

    # merge data
    merged = merge_list(Users, Scores)
    print("Merged List:", merged)

    # optimeze without modifying original list
    print("Optimized Merged List:", optimized_merge_list(Users, Scores))
    