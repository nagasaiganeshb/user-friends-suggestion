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
   This will run all the test cases in the `test.py` file

### Project Structure
-------------------

- **Server.py**: Contains the implementation of the API using Python and FastAPI. It defines the `/suggest_friends` endpoint that returns suggested friends for a given user.
  - **Python**: The server.py file is written in Python and uses the FastAPI framework to build the API.
  - **API**: The file defines the `/suggest_friends` API endpoint that accepts a JSON payload and returns a list of suggested friends.
  - **Function**: The `suggest_friends_api` function implements the logic to suggest friends based on the user's friend list and the friend lists of their friends.
- **Test.py**: Contains test cases for the API using pytest. It uses an in-memory SQLite database to test the functionality of the API.
  - **Database**: The test.py file uses an in-memory SQLite database to store and retrieve friendship data for testing purposes.
  - **Test Cases**: The file contains test cases that verify the functionality of the `/suggest_friends` API endpoint using dynamic and empty payloads.