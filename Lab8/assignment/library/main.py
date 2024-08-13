# Lab8 - Integration testing
# SC353201 Software Quality Assurance
# Semester 1/2567
# Instructor: Chitsutha Soomlek

import sqlalchemy
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, Session, relationship

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

# Database model definitions
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    firstauthor = Column(String, nullable=False)
    isbn = Column(String, nullable=False)
    not_available = relationship("Borrowlist", back_populates="borrowed_book")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    fullname = Column(String, nullable=False)
    has_book = Column(Boolean, default=False)
    holder = relationship("Borrowlist", back_populates="borrower")


# Database model definitions
class Borrowlist(Base):
    __tablename__ = "borrowlist"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    borrower = relationship("User", back_populates="holder")
    borrowed_book = relationship("Book", back_populates="not_available")

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
def create_user(username: str, fullname: str, db: Session = Depends(get_db)):
    db_user = User(username=username, fullname=fullname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/books/")
def create_book(title: str, firstauthor: str, isbn:str, db: Session = Depends(get_db)):
    db_book = Book(title=title, firstauthor=firstauthor, isbn=isbn)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.post("/borrowlist/")
def create_borrowlist(user_id: int, book_id: int, db: Session = Depends(get_db)):
    db_borrowlist = Borrowlist(user_id=user_id, book_id=book_id)
    db.add(db_borrowlist)
    db.commit()
    db.refresh(db_borrowlist)
    return db_borrowlist


@app.get("/borrowlist/{user_id}")
def get_borrowlist(user_id: int, db: Session = Depends(get_db)):
    borrowed_books = db.query(Borrowlist).filter(Borrowlist.user_id == user_id).all()
    if not borrowed_books:
        raise HTTPException(status_code=404, detail="User not found or no book being borrowed by the user")
    return borrowed_books

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

