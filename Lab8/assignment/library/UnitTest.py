# Lab8 - Integration testing
# SC353201 Software Quality Assurance
# Semester 1/2567
# Author: Paweennawat Sukruam 653380136-7 Sec.1

import pytest
from main import User, Book

#TestUser
def test_add_user(db_session):
    new_user = User(username="newuser1" , fullname="test_newuser1")
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User).filter_by(username="newuser1").first()
    assert user is not None
    assert user.username == "newuser1"

def test_delete_user(db_session):
    user = User(username="newuser2",fullname="test_newuser2")
    db_session.add(user)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    deleted_user = db_session.query(User).filter_by(username="newuser2").first()
    assert deleted_user is None

#TestBook
def test_add_book(db_session):
    new_book= Book(title="test_book", firstauthor="test_author", isbn="000-00-00000-00-0")
    db_session.add(new_book)
    db_session.commit()

    book = db_session.query(Book).filter_by(title="test_book").first()
    assert book is not None
    assert book.title == "test_book"

def test_delete_book(db_session):
    book = Book(title="book_test", firstauthor="i am", isbn="111-11-11111-11-1")
    db_session.add(book)
    db_session.commit()

    db_session.delete(book)
    db_session.commit()

    deleted_book = db_session.query(Book).filter_by(title="book_test").first()
    assert deleted_book is None