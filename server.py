from collections import deque
from typing import Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class FriendSuggestionRequest(BaseModel):
    """
    Request model for the friend suggestion API endpoint.
    """
    user_id: int
    user_friends: List[int]
    friends_of_friends: Dict[int, List[int]]

@app.post("/suggest_friends", response_model=List[int])
def suggest_friends_api(request: FriendSuggestionRequest) -> List[int]:
    """
    Endpoint to suggest friends of friends for a given user, using graph traversal (BFS).

    Args:
        request (FriendSuggestionRequest): Request containing user ID, user friends, and friends of friends.

    Returns:
        List[int]: List of suggested friends.
    """
    user_friends_set = set(request.user_friends)
    suggestions = set()
    visited = set()
    queue = deque(request.user_friends)

    while queue:
        current_friend = queue.popleft()
        for fof in request.friends_of_friends.get(current_friend, []):
            if fof != request.user_id and fof not in user_friends_set and fof not in visited:
                suggestions.add(fof)
                visited.add(fof)

    print(suggestions)
    return list(suggestions)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
