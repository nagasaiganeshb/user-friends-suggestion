import sqlite3
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

@pytest.fixture(scope="module")
def sqlite_connection():
    """
    Fixture to create an in-memory SQLite database connection.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE friendships (user_id INTEGER, friend_id INTEGER);")
    conn.commit()
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def insert_mock_data(sqlite_connection):
    """
    Fixture to insert mock friendship data into the SQLite database.
    """
    cursor = sqlite_connection.cursor()
    cursor.executemany("INSERT INTO friendships (user_id, friend_id) VALUES (?, ?);", [
        (1, 2), (1, 3),
        (2, 1), (2, 4),
        (3, 1), (3, 5),
        (4, 2),
        (5, 3)
    ])
    sqlite_connection.commit()

def test_suggest_friends_api_with_dynamic_payload(sqlite_connection, insert_mock_data):
    """
    Test case to verify the functionality of the suggest_friends API endpoint with dynamic payload.
    """
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT DISTINCT user_id FROM friendships;")
    for row in cursor.fetchall():
        user_id = row[0]

        cursor.execute("SELECT friend_id FROM friendships WHERE user_id = ?;", (user_id,))
        user_friends = [row[0] for row in cursor.fetchall()]

        friends_of_friends = {}
        for friend_id in user_friends:
            cursor.execute("SELECT friend_id FROM friendships WHERE user_id = ?;", (friend_id,))
            friends_of_friends[friend_id] = [row[0] for row in cursor.fetchall()]

        response = client.post("/suggest_friends", json={
            "user_id": user_id,
            "user_friends": user_friends,
            "friends_of_friends": friends_of_friends
        })

        assert response.status_code == 200

        cursor.execute(
            f"""
                SELECT DISTINCT f2.friend_id 
                FROM friendships f1
                LEFT JOIN friendships f2 ON f1.friend_id = f2.user_id
                WHERE f1.user_id = {user_id} AND f2.friend_id IS NOT NULL AND f2.friend_id != {user_id};
            """
        )
        expected_suggested_friends = [row[0] for row in cursor.fetchall()]

        assert sorted(response.json()) == sorted(expected_suggested_friends)

def test_suggest_friends_api_with_empty_payload():
    """
    Test case to verify the behavior of suggest_friends API endpoint with empty payload.
    """
    response = client.post("/suggest_friends", json={})

    assert response.status_code == 422
