# Lab8 - Integration testing
# Simple app - FastAPI setup, a SQL database having two tables (User and Tweet), and
# a simplified version of Twitter API.

import sqlalchemy
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./example.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

# Database model definitions
class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="tweets")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    tweets = relationship("Tweet", back_populates="author")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Routes
@app.post("/users/")
def create_user(username: str, db: Session = Depends(get_db)):
    db_user = User(username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/tweets/")
def create_tweet(user_id: int, content: str, db: Session = Depends(get_db)):
    db_tweet = Tweet(user_id=user_id, content=content)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet

@app.get("/tweets/{user_id}")
def read_tweets(user_id: int, db: Session = Depends(get_db)):
    tweets = db.query(Tweet).filter(Tweet.user_id == user_id).all()
    if not tweets:
        raise HTTPException(status_code=404, detail="User not found or no tweets")
    return tweets

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
