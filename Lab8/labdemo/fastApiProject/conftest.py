# Lab8 - Integration testing
# This file contains pytest fixture which initialize the example database.
# pytest automatically recognize the fixtures (conftest.py) during execution.

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base

# Database URL for testing purposes
SQLALCHEMY_DATABASE_URL = "sqlite:///./example.db"

# Fixture to create a database engine

@pytest.fixture(scope="session")
def engine():
    return create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Fixture to create the database tables

@pytest.fixture(scope="session")
def setup_database(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fixture for creating a new session for each test

@pytest.fixture(scope="function")
def db_session(engine, setup_database):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    connection.close()
    transaction.rollback()
