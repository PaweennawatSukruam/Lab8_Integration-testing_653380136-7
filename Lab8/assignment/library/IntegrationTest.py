import pytest
from fastapi.testclient import TestClient
from main import app, get_db, User, Book,Borrowlist

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.mark.parametrize("book_id", [1,2])
def test_create_borrowlist(client, db_session, book_id):
    user = User(username="tuser", fullname="testuser")
    db_session.add(user)
    db_session.commit()

    response = client.post(f"/borrowlist/?user_id={user.id}&book_id={book_id}")
    assert response.status_code == 200
    assert response.json()["book_id"] == book_id
    assert db_session.query(Borrowlist).filter_by(book_id=book_id).first()

@pytest.mark.parametrize("user_id", [1,2,3])
def test_get_borrowlist(client, db_session, user_id):
    user = User(username=f"user{user_id}", fullname=f"Test User {user_id}")
    db_session.add(user)
    db_session.commit()

    book = Book(title="book_test", firstauthor="i am", isbn="111-11-11111-11-1")
    db_session.add(book)
    db_session.commit()

    test_borrowlist = Borrowlist(user_id=user.id, book_id=book.id)
    db_session.add(test_borrowlist)
    db_session.commit()


    response = client.get(f"/borrowlist/{user.id}")
    assert response.status_code == 200
    if isinstance(response.json(), dict):
        assert response.json()["user_id"] == user.id
    assert len(response.json())  == 1

   