# Lab8 - Integration testing
# Integration testing - Create a test client to check the connection and interaction
# among different components of the application.

import pytest
from fastapi.testclient import TestClient
from main import app, get_db, User, Tweet

# create a test client to interact with the api
@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.mark.parametrize("username", ["test_user1", "test_user2", "test_user3"])
def test_create_user(client, db_session, username):
    # makes a POST request to the /users/ endpoint
    response = client.post(f"/users/?username={username}")

    # checks that the api request was successful
    assert response.status_code == 200

    # checks that username returned by the api matches the one we sent
    assert response.json()["username"] == username

    # checks that the user was succesfully added to the database
    assert db_session.query(User).filter_by(username=username).first()

@pytest.mark.parametrize("content", ["Hello World", "Goodbye and have good day"])
def test_create_tweet(client, db_session, content):

    # create the user to associate the tweet with
    user = User(username="testuser")
    db_session.add(user)
    db_session.commit()

    # makes a POST request to the /tweets/ endpoint
    response = client.post(f"/tweets/?user_id={user.id}&content={content}")

    # checks that the api request was successful
    assert response.status_code == 200

    # checks the content returned by the api matches the one we sent
    assert response.json()["content"] == content

    # checks that the tweet was succesfully added to the database
    assert db_session.query(Tweet).filter_by(content=content).first()
