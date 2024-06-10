from collections import deque
from typing import Dict, List, Tuple
from fastapi import FastAPI
import uvicorn

from db_handler import get_db_connection, initialize_db

app = FastAPI()
def get_user_and_friends_data(user_id: int) -> Tuple[List[int], Dict[int, List[int]]]:
    """
    Retrieve the user's friends and their friends' friends from the database.
    
    Args:
        user_id (int): The ID of the user.

    Returns:
        Tuple[List[int], Dict[int, List[int]]]: A tuple containing the list of the user's friends
                                                 and a dictionary mapping each friend to their friends.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f1.friend_id, GROUP_CONCAT(f2.friend_id)
        FROM friendships f1
        LEFT JOIN friendships f2 ON f1.friend_id = f2.user_id
        WHERE f1.user_id = ?
        GROUP BY f1.friend_id
    """, (user_id,))
    rows = cursor.fetchall()

    user_friends = [friend for friend, _ in rows]
    friends_of_friends = {
        friend: [int(fof) for fof in (fof_concat.split(',') if fof_concat else [])] for friend, fof_concat in rows
    }

    conn.close()
    return user_friends, friends_of_friends

def store_suggestions_in_db(user_id: int, suggestions: List[int]):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT OR IGNORE INTO friend_suggestions (user_id, suggested_friend_id) VALUES (?, ?)",
        [(user_id, suggestion) for suggestion in suggestions]
    )
    conn.commit()
    conn.close()

@app.get("/suggest_friends", response_model=List[int])
def suggest_friends_api(user_id: int) -> List[int]:
    user_friends, friends_of_friends = get_user_and_friends_data(user_id)
    
    user_friends_set = set(user_friends)
    suggestions = set()
    visited = set()
    queue = deque(user_friends)

    while queue:
        current_friend = queue.popleft()
        for fof in friends_of_friends.get(current_friend, []):
            if fof != user_id and fof not in user_friends_set and fof not in visited:
                suggestions.add(fof)
                visited.add(fof)

    suggestions_list = list(suggestions)
    if suggestions_list:
        store_suggestions_in_db(user_id, suggestions_list)
    return suggestions_list

if __name__ == "__main__":
    initialize_db()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
