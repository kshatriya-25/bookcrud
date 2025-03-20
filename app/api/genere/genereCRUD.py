#OM VIGHNHARTAYE NAMO NAMAH :

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from ...schemas.masterSchema import GenreCreate, GenreResponse, BookResponse
from ...modals.masters import Genre, Book, BookGenre
from ...database.session import getdb

router = APIRouter()

@router.post("/genres/", response_model=GenreResponse, tags=['genre'])
def create_genre(genre_name: str = Form(...), db: Session = Depends(getdb)):
    try:
        existing_genre = db.query(Genre).filter(Genre.genre_name == genre_name).first()
        if existing_genre:
            raise HTTPException(status_code=400, detail="Genre already exists")
        
        genre = Genre(genre_name=genre_name)
        db.add(genre)
        db.commit()
        db.refresh(genre)
        return genre
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/genres/", response_model=List[GenreResponse], tags=['genre'])
def get_genres(db: Session = Depends(getdb)):
    try:
        genres = db.query(Genre).all()
        return genres
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/genres/{genre_id}/books", response_model=List[BookResponse], tags=['genre'])
def get_books_by_genre(genre_id: int, db: Session = Depends(getdb)):
    try:
        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        
        books = (
            db.query(Book)
            .join(BookGenre, Book.id == BookGenre.book_id)
            .filter(BookGenre.genre_id == genre_id)
            .all()
        )
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
