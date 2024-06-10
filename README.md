**Friends Suggestion API**
=====================

**Getting Started**
-------------------

### Prerequisites

- Python 3.11
- pip

### Installation

1. **Create Virtual Env**: Create a new virtual environment using Python 3.11:
   ```
   python -m venv env
   ```
2. **Activate Virtual Env**: Activate the virtual environment:
   ```
   source env/bin/activate
   ```
3. **Install Requirements**: Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Server
--------------------

1. **Start Server**: Run the server using:
   ```
   python server.py
   ```
   This will start the server on `http://localhost:8000`.

### Running Test Cases
----------------------

1. **Run Tests**: Run the test cases using:
   ```
   pytest test.py
   ```
   This will run all the test cases in the `test.py` file.

### Project Structure
-------------------

- **server.py**: Contains the implementation of the API using Python and FastAPI. It defines the `/suggest_friends` endpoint that returns suggested friends for a given user.
  - **Python**: The `server.py` file is written in Python and uses the FastAPI framework to build the API.
  - **API**: The file defines the `/suggest_friends` API endpoint that accepts a user ID as a query parameter and returns a list of suggested friends.
  - **Functions**:
    - `suggest_friends_api`: Implements the logic to suggest friends based on the user's friend list and the friend lists of their friends.
    - `get_user_and_friends_data`: Retrieves the user's friends and their friends' friends from the database.
    - `store_suggestions_in_db`: Stores the suggested friends in the database.

- **db_handler.py**: Handles database connections and initialization.
  - **Functions**:
    - `initialize_db`: Initializes the database with required tables and mock data.
    - `get_db_connection`: Establishes and returns a database connection.

- **test.py**: Contains test cases for the API using pytest. It connects to the same SQLite database to test the functionality of the API.
  - **Database**: The `test.py` file uses the same SQLite database (`friends.db`) to store and retrieve friendship data for testing purposes.
  - **Test Cases**:
    - `test_suggest_friends_api_with_dynamic_payload`: Verifies the functionality of the `/suggest_friends` API endpoint with dynamic payloads, and checks that the suggested friends are saved to the database.
    - `test_suggest_friends_api_with_empty_payload`: Verifies the behavior of the `/suggest_friends` API endpoint with an empty payload.

### Example Usage
-----------------

1. **API Request**: Send a GET request to the `/suggest_friends` endpoint with a `user_id` query parameter:
   ```sh
   curl -X 'GET' \
     'http://localhost:8000/suggest_friends?user_id=1' \
     -H 'accept: application/json'
   ```
2. **API Response**: The API will return a list of suggested friends for the given user ID.
