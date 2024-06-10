import pytest
from fastapi.testclient import TestClient
from db_handler import get_db_connection
from server import app, initialize_db

client = TestClient(app)

@pytest.fixture(scope="module")
def sqlite_connection():
    """
    Fixture to create a SQLite database connection for testing.
    """
    conn = get_db_connection()
    initialize_db()
    yield conn
    conn.close()

def test_suggest_friends_api_with_dynamic_payload(sqlite_connection):
    """
    Test case to verify the functionality of the suggest_friends API endpoint with dynamic payload.
    """
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT DISTINCT user_id FROM friendships;")
    for row in cursor.fetchall():
        user_id = row[0]
        response = client.get("/suggest_friends", params={"user_id": user_id})
        assert response.status_code == 200

        cursor.execute("""
            SELECT DISTINCT f2.friend_id
            FROM friendships f1
            LEFT JOIN friendships f2 ON f1.friend_id = f2.user_id
            WHERE f1.user_id = ? AND f2.friend_id IS NOT NULL AND f2.friend_id != ?
        """, (user_id, user_id))
        expected_suggested_friends = [row[0] for row in cursor.fetchall()]
        assert sorted(response.json()) == sorted(expected_suggested_friends)

        cursor.execute("""
            SELECT suggested_friend_id
            FROM friend_suggestions
            WHERE user_id = ?
        """, (user_id,))
        saved_suggestions = [row[0] for row in cursor.fetchall()]
        assert sorted(response.json()) == sorted(saved_suggestions)

def test_suggest_friends_api_with_empty_payload():
    """
    Test case to verify the behavior of suggest_friends API endpoint with empty payload.
    """
    response = client.get("/suggest_friends", params={"user_id": None})
    assert response.status_code == 422
