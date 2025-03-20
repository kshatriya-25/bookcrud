#OM VIGHNHARTAYE NAMO NAMAH :


from ...modals.masters import *
from fastapi import APIRouter , Depends , HTTPException
from typing import List
from ...schemas.masterSchema import *
from sqlalchemy.orm import Session
from ...database.session import getdb
router = APIRouter()

from ...modals.masters import *
from fastapi import APIRouter, Depends, HTTPException, Form
from typing import List
from ...schemas.masterSchema import *
from sqlalchemy.orm import Session
from ...database.session import getdb
from pydantic import ValidationError

router = APIRouter()


@router.post("/users/register", response_model=UserResponse )
def register_user(username: str = Form(...), email: str = Form(...), db: Session = Depends(getdb)):
    try:
        user_data = UserCreate(username=username, email=email)
        db_user = User(username=user_data.username, email=user_data.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

# Books CRUD
@router.post("/books/", response_model=BookResponse, tags=['books'])
def create_book(title: str = Form(...), author_id: int = Form(...), published_year: int = Form(...), db: Session = Depends(getdb)):
    try:
        book_data = BookCreate(title=title, author_id=author_id, published_year=published_year)
        db_book = Book(title=book_data.title, author_id=book_data.author_id, published_year=book_data.published_year)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

@router.get("/books/", response_model=List[BookResponse], tags=['books'])
def get_books(title: str = None, author: str = None, min_rating: float = None, db: Session = Depends(getdb)):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.join(Author).filter(Author.name.ilike(f"%{author}%"))
    books = query.all()
    return books

@router.get("/books/{book_id}", response_model=BookResponse, tags=['books'])
def get_book(book_id: int, db: Session = Depends(getdb)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=BookResponse, tags=['books'])
def update_book(book_id: int, title: str = Form(...), author_id: int = Form(...), published_year: int = Form(...), db: Session = Depends(getdb)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    try:
        book_data = BookCreate(title=title, author_id=author_id, published_year=published_year)
        db_book.title = book_data.title
        db_book.author_id = book_data.author_id
        db_book.published_year = book_data.published_year
        db.commit()
        db.refresh(db_book)
        return db_book
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

@router.delete("/books/{book_id}", tags=['books'])
def delete_book(book_id: int, db: Session = Depends(getdb)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted"}
